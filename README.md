# vxn-py
 A python script for extracting Gameloft .vxn files.

# About vxn files

vxn files are a proprietary multistrean audio container that can be found in many Gameloft games. They can contain 1 of 4 different audio encodings, PCM, Microsoft ADPCM, Microsoft IMA ADPCM, or Musepack.

For a long time the only way to extract this audio data was by using [vgmstream](https://vgmstream.org). This posed a problem due to how vgmstream works. The audio files you get back are PCM encoded (wav files), no matter what format the audio data was originally in. Not to mention, it uses ffmpeg to transcode the Musepack format into wav files. This is an issue because of audio integrity. If you wanted to get the raw audio data from vxn files with vgmstream, you won't be able to, which also means, you can't use whatever Musepack decoder you want.

That all changes with vxn-py. This program extracts the raw data from the vxn files without any modifications. The only additions are the wav file headers so that any program knows what wav file format it's dealing with. Any vxn files that has Musepack data in them, just contains the full mpc file, including its header, so thankfully I don't have to worry about that (figuring out the wav file header was already a pain). This means that no audio data could possibly be lost, because there is no audio transcoding being done. You can then do whatever you want with the data, including using other Musepack decoders (because some mpc files don't decode very well in ffmpeg).

Unfortunately, this program does not create vxn files, mainly because there's still other chunks that I don't know how to read yet.

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
