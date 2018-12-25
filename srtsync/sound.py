#!/usr/bin/env python3
# coding: utf-8
"""
Extract audio from a video file
Read wave file
"""

from subprocess import check_call
from pathlib import Path
import sys
import wave
import datetime


def read_wave(path):
    """Reads a .wav file.
    Takes the path, and returns (PCM audio data, sample rate).
    """
    with wave.open(path, 'rb') as wave_file:
        num_channels = wave_file.getnchannels()
        assert num_channels == 1
        sample_width = wave_file.getsampwidth()
        assert sample_width == 2
        sample_rate = wave_file.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wave_file.readframes(wave_file.getnframes())
        length = len(pcm_data) / sample_rate / 2
        return pcm_data, sample_rate, length


def extract(video, audio):
    """
    Extract audio from video_file
    """
    if not isinstance(video, Path):
        video = Path(video)

    if not isinstance(audio, Path):
        audio = Path(audio)

    command = ("ffmpeg -loglevel panic -i".split() + [str(video)] +
               "-ab 160k -ac 1 -ar 48000 -vn".split() + [audio])
    print("Extracting audio...")
    check_call(command)

    return read_wave(str(audio))


if __name__ == "__main__":
    video_file = sys.argv[1]
    audio_file = sys.argv[2]

    audio, sample_rate, length = extract(video_file, audio_file)
    print(f"Audio extracted.\n"
          f"  Sample rate = {sample_rate}Hz\n"
          f"  Length = {datetime.timedelta(seconds=length)}")
