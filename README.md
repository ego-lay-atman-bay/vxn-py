# vxn-py
 A python script for decoding Gameloft .vxn files.

# Installation

Install with python

```shell
pip install vxn-py
```

# Usage

```shell
python -m vxn extract "file.vxn"
python -m vxn extract -h
vxndec "file.vxn"
vxndec -h
```

Or within code.

```python
from vxn import VXN

v = VXN('path/to/file.vxn')

v.streams[0].save(f'out.{v.streams[0].EXTENSION}')
```
