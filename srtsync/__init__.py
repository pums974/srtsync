#!/usr/bin/env python3
# coding: utf-8
"""
Automatic synchronizer of subtitles based on voice activity in the video
"""

__version__ = "1.0.1"

from srtsync.tools import sync
from srtsync.sound import extract as extract_audio
from srtsync.vad import extract_from_video as extract_voice_activity
from srtsync.srt import read as read_srt
from srtsync.srt import transform as transform_srt
from srtsync.srt import write as write_srt
from srtsync.srt import to_timestamps as srt_to_timestamps
