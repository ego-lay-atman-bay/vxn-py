import struct
from typing import Annotated

import dataclasses_struct as dcs

from .audioformat import AudioFormat


@dcs.dataclass()
class RIFFHeader():
    magic: Annotated[bytes, 4] = b'RIFF'
    chunk_size: dcs.U32 = 0

@dcs.dataclass()
class WAVEHeader():
    magic: Annotated[bytes, 4] = b'WAVE'

@dcs.dataclass()
class FormatHeader():
    fmt: Annotated[bytes, 4] = b'fmt '
    chunk_size: dcs.U32 = 0
    format_tag: dcs.U32 = 0

class WAV(AudioFormat):
    EXTENSION = 'wav'
    MAGIC = b'RIFF'
    
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
        super().__init__(data)
        
        self.block_align = block_align
        self.sample_rate = sample_rate
        self.num_samples = num_samples
        self.stream_size = stream_size
        self.channels = channels
        self.bits = bits
    
    def create_format_header(self) -> bytes:
        return b''
    
    def create_header(self) -> bytes:
        riff_header = RIFFHeader()
        wav_header = WAVEHeader()
        format_header = self.create_format_header()

        data = self.create_data_chunk()

        riff_header.chunk_size = wav_header.__dataclass_struct__.size + \
                                 len(format_header) + \
                                 len(data)
        
        result = riff_header.pack() + wav_header.pack() + format_header + data
        
        return result
    
    def create_data_chunk(self) -> bytes:
        return struct.pack(
            '4sI',
            b'data',
            len(self.data),
        ) + self.data
