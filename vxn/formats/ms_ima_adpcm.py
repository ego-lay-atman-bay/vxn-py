import dataclasses_struct as dcs
from typing import Annotated
import struct

from .wav import WAV

@dcs.dataclass_struct(size = 'std')
class MS_IMA_ADPCMHeader():
    fmt: Annotated[bytes, 4] = b'fmt '
    chunk_size: dcs.U32 = 0
    format_tag: dcs.U16 = 17
    channels: dcs.U16 = 0
    sample_rate: dcs.U32 = 0
    average_bytes_per_second: dcs.U32 = 0
    block_align: dcs.U16 = 0
    bits_per_sample: dcs.U16 = 0

@dcs.dataclass_struct(size = 'std')
class MS_IMA_ADPCMExtendedData():
    size: dcs.U16 = 2
    samples_per_block: dcs.U16 = 0

@dcs.dataclass_struct(size = 'std')
class MS_IMA_ADPCMFact():
    chunk_id: Annotated[bytes, 4] = b'fact'
    chunk_size: dcs.U32 = 4
    uncompressed_size: dcs.U32 = 0

class MS_IMA_ADPCM(WAV):
    ENCODING = 'Microsoft 4-bit IMA ADPCM'
    
    
    def create_format_header(self):
        header = MS_IMA_ADPCMHeader(
            channels = self.channels,
            sample_rate = self.sample_rate,
            # average_bytes_per_second = (self.sample_rate * self.bits * self.channels) // 8,
            average_bytes_per_second = self.sample_rate,
            block_align = self.block_align,
            bits_per_sample = 4,
        )
        
        extended_data = MS_IMA_ADPCMExtendedData(
            # samples_per_block = (((self.block_align - (7 * self.channels)) * 8) // (self.bits * self.channels)) + 2,
            samples_per_block = 1017, # I do not know what to put here
        )
        
        extended_data.size = (extended_data.__dataclass_struct__.size - 2)
        
        header.chunk_size = (header.__dataclass_struct__.size - 8) + extended_data.__dataclass_struct__.size
        # header.chunk_size = self.num_samples * 4
        
        fact = MS_IMA_ADPCMFact(
            uncompressed_size = self.num_samples,
        )
        
        return header.pack() + extended_data.pack() + fact.pack()

    def get_riff_chunk_size(self, wav_header: bytes, format_header: bytes, data: bytes):
        return self.num_samples * 4
