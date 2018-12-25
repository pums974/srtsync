#!/usr/bin/env python3
# coding: utf-8
"""
Automatic synchronizer of subtitles based on video or other subtitle
"""

__version__ = "1.1.0"

from srtsync.tools import sync
from srtsync.tools import is_video, is_srt
from srtsync.sound import extract as extract_audio
from srtsync.vad import extract_from_video as extract_voice_activity
from srtsync.srt import read as read_srt
from srtsync.srt import transform as transform_srt
from srtsync.srt import write as write_srt
from srtsync.srt import to_timestamps as srt_to_timestamps
