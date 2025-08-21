import dataclasses_struct as dcs
from typing import Annotated

from .wav import WAV

@dcs.dataclass_struct(size = 'std')
class PCMHeader():
    fmt: Annotated[bytes, 4] = b'fmt '
    chunk_size: dcs.U32 = 16
    format_tag: dcs.U16 = 1
    channels: dcs.U16 = 0
    sample_rate: dcs.U32 = 0
    average_bytes_per_second: dcs.U32 = 0
    block_align: dcs.U16 = 0
    bits_per_sample: dcs.U16 = 0

class PCM(WAV):
    @property
    def ENCODING(self):
        return f'{self.bits}-bit Little Endian PCM'
    
    def create_format_header(self) -> bytes:
        header = PCMHeader(
            channels = self.channels,
            sample_rate = self.sample_rate,
            average_bytes_per_second = (self.sample_rate * self.bits * self.channels) / 8,
            block_align = self.block_align,
            bits_per_sample = self.bits,
        )
        
        return header.pack()
