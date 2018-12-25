#!/bin/env/python3
# coding: utf-8
"""
Subtitle reader and writer
"""
import datetime

import pysrt


def read(srtfile):
    """Read subtitle"""
    return pysrt.open(srtfile)


def to_timestamps(subs):
    """Convert subtitles to timstamps"""
    srt = [(str(sub.start), str(sub.end))
           for sub in subs]
    srt = [(datetime.datetime.strptime(start, "%H:%M:%S,%f"),
            datetime.datetime.strptime(end, "%H:%M:%S,%f"))
           for start, end in srt]
    srt = [(datetime.timedelta(hours=start.hour,
                               minutes=start.minute,
                               seconds=start.second,
                               milliseconds=start.microsecond / 1000).total_seconds(),
            datetime.timedelta(hours=end.hour,
                               minutes=end.minute,
                               seconds=end.second,
                               milliseconds=end.microsecond / 1000).total_seconds())
           for start, end in srt]
    return srt


def transform(subs, stretch=1., shift=0):
    """transform subtitles"""
    subs.shift(ratio=stretch)
    subs.shift(seconds=shift)
    return subs


def write(subs, outfile):
    """write subtitles"""
    subs.save(outfile)
