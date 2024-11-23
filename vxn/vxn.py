import io
import os
import struct
from contextlib import nullcontext
from typing import Annotated, BinaryIO

import dataclasses_struct as dcs

from .file_utils import is_binary_file, is_text_file, is_eof, get_filesize
from .formats import MPC, PCM, MS_ADPCM, MS_IMA_ADPCM


@dcs.dataclass()
class Header():
    version: Annotated[bytes, 8] = b'0.0.1\x00\x00\x00'
    filesize: dcs.U32 = 0
    unknown: Annotated[bytes, 4] = b'\x00\x00\x00\x00'

@dcs.dataclass()
class Afmt():
    codec: dcs.U16
    channels: dcs.U16
    sample_rate: dcs.U32
    block_align: dcs.U16
    bits: dcs.I16
    
@dcs.dataclass()
class SegmStream():
    stream_offset: dcs.U32
    stream_size: dcs.U32
    num_samples: dcs.U32
    unknown: Annotated[bytes, 4*3]
    

class VXN():
    EXTENSION = 'vxn'
    MAGIC = b'VoxN'
    MIME = 'audio/x-vxn'
    
    def __init__(self, file: str | bytes | bytearray | BinaryIO | None = None) -> None:
        self.header = Header()
        self.chunks = {}
        self.format: Afmt | None = None
        self.streams_data: list[SegmStream] = []
        self.streams: list[PCM | MS_ADPCM | MS_IMA_ADPCM | MPC] = []
        self.coefs: list[tuple[int]] = []

        if file != None:
            self.read(file)
    
    def read(self, file: str | bytes | bytearray | BinaryIO):
        if isinstance(file, str) and os.path.isfile(file):
            context_manager = open(file, 'rb')
        elif isinstance(file, (bytes, bytearray)):
            context_manager = io.BytesIO(file)
        elif is_binary_file(file):
            context_manager = nullcontext(file)
        elif is_text_file(file):
            raise TypeError('file must be open in binary mode')
        else:
            raise TypeError('cannot open file')
        
        self.header = Header()
        self.chunks = {}
        self.format: Afmt | None = None
        self.streams_data: list[SegmStream] = []
        self.streams: list[PCM | MS_ADPCM | MS_IMA_ADPCM | MPC] = []
        self.coefs: list[tuple[int]] = []
        
        self.chunks = {}
        
        with context_manager as open_file:
            self.header = self._read_header(open_file)
            
            while not is_eof(open_file):
                id, data = self._read_chunk(open_file)
                self.chunks[id] = data
            
            self.format = Afmt.from_packed(self.chunks['Afmt'])
            self.streams_data = self._read_segm(self.chunks['Segm'])
            
            if 'Msae' in self.chunks:
                self.coefs = [
                    coef for coef in
                    struct.iter_unpack(
                        'hh',
                        self.chunks['Msae'][4:4 + (struct.unpack(
                            'H',
                            self.chunks['Msae'][2:4],
                        )[0] * 4)]
                    )
                ]
            
            self.streams = self._read_audio_data(self.chunks['Data'])
    
    
    def _read_header(self, file: BinaryIO) -> Header:
        """Read the header of a `.vxn` file.

        Args:
            file (IO): File-like object.

        Returns:
            dict: Header.
        """
        
        magic, data = self._read_chunk(file)
        
        if not self.check_magic(magic.encode()):
            raise ValueError('File is not vxn file')
        
        header: Header = Header.from_packed(data)

        if get_filesize(file) != header.filesize:
            raise ValueError('File is not the same filesize as suggested in the file')
        
        return header
            
    
    @classmethod
    def check_magic(cls, magic: Annotated[bytes, 4]):
        return magic[0:4] == cls.MAGIC
    
    def _read_chunk(self, file: BinaryIO) -> tuple[str, bytes]:
        format = '4s1I'
        size: int
        id: bytes
        id, size = struct.unpack(
            format,
            file.read(struct.calcsize(format)),
        )
        id: str = id.decode()
        data = file.read(size)

        return id, data
    
    def _read_segm(self, buffer: bytes):
        num_streams = struct.unpack('I', buffer[0:struct.calcsize('I')])[0]
        streams = []
        
        for stream in struct.iter_unpack(
            SegmStream.__dataclass_struct__.format,
            buffer[4:4 + (num_streams * SegmStream.__dataclass_struct__.size)],
        ):
            streams.append(SegmStream(*stream))
        
        return streams
    
    def _read_audio_data(self, buffer: bytes):
        result = []
        
        match self.format.codec:
            case 0x0001:
                assert self.format.bits == 16
                
                for stream in self.streams_data:
                    result.append(PCM(
                        buffer[stream.stream_offset:stream.stream_offset + stream.stream_size],
                        block_align = self.format.block_align,
                        sample_rate = self.format.sample_rate,
                        num_samples = stream.num_samples,
                        stream_size = stream.stream_size,
                        channels = self.format.channels,
                        bits = self.format.bits,
                    ))
            
            case 0x0002:
                assert self.format.bits == 4
                
                for stream in self.streams_data:
                    result.append(MS_ADPCM(
                        buffer[stream.stream_offset:stream.stream_offset + stream.stream_size],
                        block_align = self.format.block_align,
                        sample_rate = self.format.sample_rate,
                        num_samples = stream.num_samples,
                        stream_size = stream.stream_size,
                        channels = self.format.channels,

                        coefs = self.coefs,
                        bits = self.format.bits,
                    ))
            
            case 0x0011:
                assert self.format.bits in [4, 16] # 16=common, 4=Asphalt Injection (Vita)

                for stream in self.streams_data:
                    result.append(MS_IMA_ADPCM(
                        buffer[stream.stream_offset:stream.stream_offset + stream.stream_size],
                        block_align = self.format.block_align,
                        sample_rate = self.format.sample_rate,
                        num_samples = stream.num_samples,
                        stream_size = stream.stream_size,
                        channels = self.format.channels,

                        bits = self.format.bits,
                    ))
            
            case 0x0800: # Musepack
                assert self.format.bits == -1, 'failed to decode musepack data'

                for stream in self.streams_data:
                    result.append(MPC(
                        buffer[stream.stream_offset:stream.stream_offset + stream.stream_size],

                        block_align = self.format.block_align,
                        sample_rate = self.format.sample_rate,
                        num_samples = stream.num_samples,
                        stream_size = stream.stream_size,
                        channels = self.format.channels,
                        bits = self.format.bits,
                    ))
        
        return result
    
    @property
    def metadata(self):
        return {
            'sample_rate': self.format.sample_rate,
            'channels': self.format.channels,
            'stream_count': len(self.streams),
        }
