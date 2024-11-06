from abc import abstractmethod

class AudioFormat():
    EXTENSION = ''
    MAGIC = b''
    MIME = ''
    
    data: bytes = b''
    
    def __init__(self, data: bytes) -> None:
        self.data = bytes(data)
    
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
