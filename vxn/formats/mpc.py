from .audioformat import AudioFormat

class MPC(AudioFormat):
    EXTENSION = 'mpc'
    MAGIC = b'MPCKSH'
