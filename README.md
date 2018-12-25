# srtsync
Automatic synchronizer of subtitles based on video or other subtitle

Largely inspired by [py-webrtcvad](https://github.com/wiseman/py-webrtcvad)

It can only stretch and shift subtitles for now.

The synchronization to another subtitle is less accurate and EXPERIMENTAL

## Getting Started
### Dependencies
 * ffmpeg for audio extraction
 * numpy / scipy for synchronization
 * pysrt for reading and writing subtitles
 optionnally
 * pymediainfo for accurate detection of a video file
 * webrtcvad for voice activity detection

### Install
pip install srtsync

### Usage
```
usage: srtsync [-h] [-a aggressiveness] source input.srt output.srt

Automatic synchronizer of subtitles based on video or other subtitle

positional arguments:
  source             path to the source (a video file or another subtitle)
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
