from typing import IO, BinaryIO, overload
import io

import os

def is_eof(f: IO):
    s = f.read(1)
    if s != b'':    # restore position
        f.seek(-1, os.SEEK_CUR)
    return s == b''

def peek(f: IO, n: int):
    s = f.read(n)
    f.seek(-len(s), os.SEEK_CUR)
    return s


def is_text_file(file: IO):
    return isinstance(file, io.TextIOBase)


def is_binary_file(file: IO):
    return isinstance(file, (io.RawIOBase, io.BufferedIOBase))

def get_filesize(file: IO):
    pos = file.tell()
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(pos)
    return size

@overload
def read_ascii_string(file: bytes) -> str: ...
@overload
def read_ascii_string(file: BinaryIO, length: int = 64) -> str: ...
def read_ascii_string(file: BinaryIO | bytes, length: int = 64) -> str:
    if isinstance(file, (bytes, bytearray)):
        data = file
    else:
        data = file.read(length)

    return data.split(b'\x00', 1)[0].decode('ascii', errors='ignore')
