import struct
from typing import Annotated

import dataclasses_struct as dcs

from .audioformat import AudioFormat

@dcs.dataclass_struct(size = 'std')
class RIFFHeader():
    magic: Annotated[bytes, 4] = b'RIFF'
    chunk_size: dcs.U32 = 0


@dcs.dataclass_struct(size = 'std')
class WAVEHeader():
    magic: Annotated[bytes, 4] = b'WAVE'

@dcs.dataclass_struct(size = 'std')
class FormatHeader():
    fmt: Annotated[bytes, 4] = b'fmt '
    chunk_size: dcs.U32 = 0
    format_tag: dcs.U32 = 0

@dcs.dataclass_struct(size = 'std')
class WAV_DATA():
    riff: RIFFHeader
    wave: WAVEHeader
    format_header: FormatHeader

class WAV(AudioFormat):
    EXTENSION = 'wav'
    MAGIC = b'RIFF'
    MIME = 'audio/x-wav'
    
    FORMAT_HEADER = FormatHeader
    
    def __init__(
        self,
        data: bytes,
        block_align: int,
        sample_rate: int,
        num_samples: int,
        stream_size: int,
        channels: int,
        bits: int = 16,
    ) -> None:
        super().__init__(
            data,
            block_align,
            sample_rate,
            num_samples,
            stream_size,
            channels,
            bits,
        )
    
    def create_format_header(self) -> bytes:
        return b''
    
    def get_riff_chunk_size(
        self,
        wav_header: bytes,
        format_header: bytes,
        data: bytes,
    ):
        return len(wav_header) + len(format_header) + len(data)
    
    def create_header(self) -> bytes:
        riff_header = RIFFHeader()
        wav_header = WAVEHeader()
        format_header = self.create_format_header()

        data = self.create_data_chunk()
        
        packed_wav = wav_header.pack()

        riff_header.chunk_size = self.get_riff_chunk_size(packed_wav, format_header, data)
        
        result = riff_header.pack() + packed_wav + format_header
        
        return result
    
    def create_data_chunk(self) -> bytes:
        return struct.pack(
            '4sI',
            b'data',
            len(self.data),
        ) + self.data
