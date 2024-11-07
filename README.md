# vxn-py
 A python script for decoding Gameloft .vxn files.

# Installation

Install with python

```shell
pip install git+[https://ego](https://github.com/ego-lay-atman-bay/vxn-py)
```

Update

```shell
pip install --upgrade git+[https://ego](https://github.com/ego-lay-atman-bay/vxn-py) --force
```

# Usage

```python
from vxn import VXN

v = VXN('path/to/file.vxn')

v.streams[0].save('out.wav') # or 'out.mpc'
```
