import dataclasses_struct as dcs
from typing import Annotated
import struct

from .wav import WAV

@dcs.dataclass_struct(size = 'std')
class MS_ADPCMHeader():
    fmt: Annotated[bytes, 4] = b'fmt '
    chunk_size: dcs.U32 = 0
    format_tag: dcs.U16 = 2
    channels: dcs.U16 = 0
    sample_rate: dcs.U32 = 0
    average_bytes_per_second: dcs.U32 = 0
    block_align: dcs.U16 = 0
    bits_per_sample: dcs.U16 = 0

@dcs.dataclass_struct(size = 'std')
class MS_ADPCMExtendedData():
    size: dcs.U16 = 32
    samples_per_block: dcs.U16 = 0
    num_coef: dcs.U16 = 0

@dcs.dataclass_struct(size = 'std')
class MS_ADPCMFact():
    chunk_id: Annotated[bytes, 4] = b'fact'
    chunk_size: dcs.U32 = 4
    uncompressed_size: dcs.U32 = 0

class MS_ADPCM(WAV):
    @property
    def ENCODING(self):
        return f'Microsoft {self.bits}-bit ADPCM'
    
    def __init__(
        self,
        data: bytes,
        block_align: int,
        sample_rate: int,
        num_samples: int,
        stream_size: int,
        channels: int,
        coefs: list[tuple[int, int]],
        bits: int = 4,
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
        self.coefs = coefs
    
    def create_format_header(self):
        header = MS_ADPCMHeader(
            channels = self.channels,
            sample_rate = self.sample_rate,
            average_bytes_per_second = (self.sample_rate * self.bits * self.channels) // 8,
            block_align = self.block_align,
            bits_per_sample = self.bits,
        )
        
        coefs = b''.join(
            struct.pack('hh', *coef) for coef in self.coefs
        )
        
        extended_data = MS_ADPCMExtendedData(
            samples_per_block = (((self.block_align - (7 * self.channels)) * 8) // (self.bits * self.channels)) + 2,
            num_coef = len(self.coefs),
        )
        
        extended_data.size = (extended_data.__dataclass_struct__.size - 2) + len(coefs)
        
        header.chunk_size = (header.__dataclass_struct__.size - 8) + extended_data.__dataclass_struct__.size + len(coefs)
        
        fact = MS_ADPCMFact(
            uncompressed_size = self.num_samples,
        )
        
        return header.pack() + extended_data.pack() + coefs + fact.pack()
