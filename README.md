# srtsync
Automatic synchronizer of subtitles based on voice activity in the video

Largely inspired by [py-webrtcvad](https://github.com/wiseman/py-webrtcvad)

It can only stretch and shift subtitles for now.

## Getting Started
### Dependencies
 * ffmpeg for audio extraction
 * numpy / scipy for synchronization
 * webrtcvad for voica activity detection
 * pysrt for reading and writing subtitles

### Install
pip install srtsync

### Usage
```
usage: srtsync [-h] [-a aggressiveness] video.avi input.srt output.srt

Automatic synchronizer of subtitles based on voice activity in the video

positional arguments:
  video.avi          path to the video file
  input.srt          path to the input subtitles file
  output.srt         path to the output subtitles file

optional arguments:
  -h, --help         show this help message and exit
  -a aggressiveness  aggressiveness in voice activity detection
```
## Author
 - **Alexandre Poux**
 
## Licence
 This work is released under the GPLv3 - see LICENSE for details
