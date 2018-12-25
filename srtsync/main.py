#!/usr/bin/env python3
# coding: utf-8
"""
Automatic synchronizer of subtitles based on video or other subtitle

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
from srtsync import is_video, is_srt


def main():
    """Executable"""
    parser = argparse.ArgumentParser(prog='srtsync',
                                     description="Automatic synchronizer of subtitles"
                                                 " based on video or other subtitle")

    parser.add_argument('-a',
                        metavar='aggressiveness',
                        default=3,
                        type=int,
                        help='aggressiveness in voice activity detection')
    parser.add_argument('source',
                        help='path to a source (a video file or another subtitle)')
    parser.add_argument('input',
                        metavar='input.srt',
                        help='path to the input subtitles file')
    parser.add_argument('output',
                        metavar='output.srt',
                        help='path to the output subtitles file')
    args = parser.parse_args()

    sourcefile = Path(args.source)
    if not sourcefile.exists():
        raise FileNotFoundError("The source file must exists !")

    input_srt = Path(args.input)
    if not input_srt.exists():
        raise FileNotFoundError("The input subtitles must exists !")

    output_srt = Path(args.output)
    if not output_srt.exists():
        warn("The output subtitle will be overwritten !")

    if is_srt(sourcefile):
        subs = read_srt(sourcefile)
        source = srt_to_timestamps(subs)
        length = None
    elif is_video(sourcefile):
        aggressiveness = args.a
        source, length = extract_voice_activity(sourcefile, aggressiveness=aggressiveness)
    else:
        raise ValueError("The source must be a subtitle of a video file !")

    subs = read_srt(input_srt)

    # For testing purposes
    if False:
        shift = 15
        stretch = 1.2
        print(f"Adding artifical shift and stretch:\n"
              f"Shift {shift:.3f} and stretch 1/{1/stretch:.3f}\n")
        subs = transform_srt(subs,
                             stretch=stretch,
                             shift=shift)

    srt = srt_to_timestamps(subs)

    shift, stretch = sync(source, srt, length)
    print(f"Shift {shift:.3f} and stretch {stretch:.3f}\n")

    subs = transform_srt(subs,
                         stretch=stretch,
                         shift=shift)

    write_srt(subs, output_srt)


if __name__ == "__main__":
    main()
