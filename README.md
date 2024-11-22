# vxn-py
 A python script for decoding Gameloft .vxn files.

# Installation

Install with python

```shell
pip install git+https://github.com/ego-lay-atman-bay/vxn-py
```

Update

```shell
pip install --upgrade git+https://github.com/ego-lay-atman-bay/vxn-py --force
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
