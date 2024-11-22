from abc import abstractmethod

class AudioFormat():
    EXTENSION = ''
    MAGIC = b''
    MIME = 'audio/x-raw'
    ENCODING = 'RAW'
    
    data: bytes = b''
    
    @property
    def duration(self) -> float:
        """Duration in seconds

        Returns:
            float: Duration in seconds.
        """
        
        return self.num_samples / self.sample_rate
    
    
    def __init__(
        self,
        data: bytes,
        block_align: int,
        sample_rate: int,
        num_samples: int,
        stream_size: int,
        channels: int,
        bits: int,
    ) -> None:
        self.data = bytes(data)
        
        self.block_align = block_align
        self.sample_rate = sample_rate
        self.num_samples = num_samples
        self.stream_size = stream_size
        self.channels = channels
        self.bits = bits
    
    def create_header(self) -> bytes:
        return b''
    
    def create_data_chunk(self) -> bytes:
        return self.data
    
    def create_file(self) -> bytes:
        result = b''
        
        result += self.create_header()
        result += self.create_data_chunk()
        
        return result
    
    def save(self, filename: str):
        data = self.create_file()
        
        with open(filename, 'wb') as file:
            file.write(data)
    
    @property
    def metadata(self):
        return {
            'encoding': self.ENCODING,
            'mime': self.MIME,
            'extension': self.EXTENSION,
            'sample_rate': self.sample_rate,
            'channels': self.channels,
            'samples': self.num_samples,
            'duration': self.duration,
        }
