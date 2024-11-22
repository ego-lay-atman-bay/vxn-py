from .audioformat import AudioFormat

class MPC(AudioFormat):
    EXTENSION = 'mpc'
    MAGIC = b'MPCKSH'
    ENCODING = 'Musepack SV8'
    MIME = 'audio/musepack'
