__version__ = '1.0.1'
__author__ = 'ego-lay-atman-bay'

from .vxn import VXN
from . import formats

def register_filetypes():
    """Register filetypes for VXN and MPC in the `filetype` module.
    """
    
    from filetype import filetype
    
    class VXNType(filetype.Type):
        MIME = VXN.MIME
        EXTENSION = VXN.EXTENSION
        
        def __init__(self):
            super().__init__(
                self.MIME,
                self.EXTENSION,
            )
        
        def match(self, buf: bytes):
            return VXN.check_magic(buf)
    
    filetype.add_type(VXNType())
    
    class MPCType(filetype.Type):
        MIME = formats.MPC.MIME
        EXTENSION = formats.MPC.EXTENSION
        
        def __init__(self):
            super().__init__(
                self.MIME,
                self.EXTENSION,
            )
        
        def match(self, buf: bytes):
            return buf[0:4] == b'MPCK'
    
    filetype.add_type(MPCType())

try:
    register_filetypes()
except:
    pass
