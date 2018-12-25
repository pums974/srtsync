#!/bin/env/python3
# coding: utf-8
"""
Detect voice activity and return a list of timestamp
"""
import collections
import sys
import datetime
from pathlib import Path
from tempfile import mkdtemp
import webrtcvad

from srtsync.sound import extract as extract_audio
from srtsync.sound import read_wave


class Frame():
    """Represents a "frame" of audio data."""
    def __init__(self, _bytes, timestamp, duration):
        self.bytes = _bytes
        self.timestamp = timestamp
        self.duration = duration


def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from PCM audio data.
    Takes the desired frame duration in milliseconds, the PCM data, and
    the sample rate.
    Yields Frames of the requested duration.
    """
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


def vad_collector(sample_rate, frame_duration_ms,
                  padding_duration_ms, vad, frames):
    """Filters out non-voiced audio frames.
    Given a webrtcvad.Vad and a source of audio frames, yields only
    the voiced audio.
    Uses a padded, sliding window algorithm over the audio frames.
    When more than 90% of the frames in the window are voiced (as
    reported by the VAD), the collector triggers and begins yielding
    audio frames. Then the collector waits until 90% of the frames in
    the window are unvoiced to detrigger.
    The window is padded at the front and back to provide a small
    amount of silence or the beginnings/endings of speech around the
    voiced frames.
    Arguments:
    sample_rate - The audio sample rate, in Hz.
    frame_duration_ms - The frame duration in milliseconds.
    padding_duration_ms - The amount to pad the window, in milliseconds.
    vad - An instance of webrtcvad.Vad.
    frames - a source of audio frames (sequence or generator).
    Returns: A generator that yields PCM audio data.
    """
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    start = 0
    frame = None
    # We use a deque for our sliding window/ring buffer.
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    # We have two states: TRIGGERED and NOTTRIGGERED. We start in the
    # NOTTRIGGERED state.
    triggered = False
    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)

        if not triggered:
            ring_buffer.append((frame, is_speech))
            num_voiced = len([f for f, speech in ring_buffer if speech])
            # If we're NOTTRIGGERED and more than 90% of the frames in
            # the ring buffer are voiced frames, then enter the
            # TRIGGERED state.
            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                start = ring_buffer[0][0].timestamp
                ring_buffer.clear()
        else:
            # We're in the TRIGGERED state, so collect the audio data
            # and add it to the ring buffer.
            ring_buffer.append((frame, is_speech))
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])
            # If more than 90% of the frames in the ring buffer are
            # unvoiced, then enter NOTTRIGGERED and yield whatever
            # audio we've collected.
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                end = frame.timestamp + frame.duration
                triggered = False
                yield start, end
                ring_buffer.clear()
    if triggered:
        end = frame.timestamp + frame.duration
        yield start, end


def extract_from_audio(audio, sample_rate, aggressiveness=3):
    """Extract timestamp of voice activity from an audio file"""
    vad = webrtcvad.Vad(aggressiveness)
    frames = frame_generator(30, audio, sample_rate)
    return list(vad_collector(sample_rate, 30, 300, vad, frames))


def extract_from_video(video, aggressiveness=3):
    """Extract timestamp of voice activity from aa video file"""

    tmp_wav = Path(mkdtemp()) / 'tmp.wav'

    audio, sample_rate, length = extract_audio(video, tmp_wav)
    voice_activity = extract_from_audio(audio, sample_rate, aggressiveness=aggressiveness)

    tmp_wav.unlink()
    tmp_wav.parent.rmdir()

    return voice_activity, length


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) != 2:
        sys.stderr.write('Usage: vad.py <aggressiveness> <path to wav file>\n')
        sys.exit(1)

    aggressiveness, audiofile = args

    audio, sample_rate, length = read_wave(audiofile)
    va = extract_from_audio(audio, sample_rate, aggressiveness=aggressiveness)

    for start, end in va:
        print(f"{datetime.timedelta(seconds=start)}"
              f" -- >"
              f"{datetime.timedelta(seconds=end)}")
