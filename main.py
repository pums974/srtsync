#!/bin/env/python3
# coding: utf-8
"""
Automatic synchronizer of subtitles based on voice activity in the video

Largely inspired by [py-webrtcvad](https://github.com/wiseman/py-webrtcvad)
"""
import argparse
from pathlib import Path
from warnings import warn
from srtsync import extract_voice_activity
from srtsync import read_srt
from srtsync import transform_srt
from srtsync import write_srt
from srtsync import srt_to_timestamps
from srtsync import sync

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='srtsync',
                                     description="Automatic synchronizer of subtitles"
                                                 " based on voice activity in the video")
    parser.add_argument('-a',
                        metavar='aggressiveness',
                        default=3,
                        type=int,
                        help='aggressiveness in voice activity detection')
    parser.add_argument('video',
                        help='path to the video file')
    parser.add_argument('input',
                        help='path to the input subtitles file')
    parser.add_argument('output',
                        help='path to the output subtitles file')
    args = parser.parse_args()

    videofile = Path(args.video)
    if not videofile.exists():
        raise FileNotFoundError("The video file must exists !")

    input_srt = Path(args.input)
    if not videofile.exists():
        raise FileNotFoundError("The input subtitles must exists !")

    output_srt = Path(args.output)
    if not videofile.exists():
        warn("The output subtitle will be overwritten !")

    aggressiveness = args.a
    voice_activity, length = extract_voice_activity(videofile, aggressiveness=aggressiveness)

    subs = read_srt(input_srt)

    # For testing purposes
    if True:
        shift = 15
        stretch = 1.2
        print(f"Adding artifical shift and stretch:\n"
              f"Shift {shift:.3f} and stretch 1/{1/stretch:.3f}\n")
        subs = transform_srt(subs,
                             stretch=stretch,
                             shift=shift)

    srt = srt_to_timestamps(subs)

    shift, stretch = sync(voice_activity, srt, length)
    print(f"Shift {shift:.3f} and stretch {stretch:.3f}\n")

    subs = transform_srt(subs,
                         stretch=stretch,
                         shift=shift)

    write_srt(subs, output_srt)
