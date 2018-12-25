#!/usr/bin/env python3
# coding: utf-8
"""
Where the magic happens
"""
import numpy as np
import scipy
import scipy.optimize


def discretize_timestamp(timestamps, stretch=1., chunk=0.1, nelem=None):
    """Convert a list of timestamps to an array of 0 and 1"""
    if nelem is None:
        nelem = max(timestamps, key=lambda x: x[1])[1]
        nelem = int(np.ceil(nelem / chunk))

    array = np.zeros(nelem)
    for start, end in timestamps:
        start = int(np.floor(stretch * start / chunk))
        end = int(np.ceil(stretch * end / chunk))
        array[start:end] = 1

    return array


def opt_shift(stretch, disc_voice_activity, srt, chunk=0.1):
    """Find the optimal shift"""
    try:
        if len(stretch) > 1:
            raise ValueError("stretch must be a single value")
        else:
            stretch = stretch[0]
    except TypeError:
        pass

    disc_srt = discretize_timestamp(srt,
                                    stretch=stretch,
                                    chunk=chunk,
                                    nelem=len(disc_voice_activity))

    nfft = 1 + 2 * len(disc_voice_activity)

    va_fft = scipy.fft(disc_voice_activity, nfft)
    srt_fft = scipy.fft(disc_srt, nfft)
    va_fft_conj = -va_fft.conjugate()
    srt_fft_conj = -srt_fft.conjugate()
    corr1 = np.abs(scipy.ifft(va_fft_conj * srt_fft))
    corr2 = np.abs(scipy.ifft(va_fft * srt_fft_conj))
    shift1 = np.argmax(corr1)
    shift2 = np.argmax(corr2)

    if corr1[shift1] > corr2[shift2]:
        return -shift1 * chunk, corr1[shift1]
    else:
        return shift2 * chunk, corr2[shift2]


def sync(voice_activity, srt, length, chunk=0.1):
    """Sync srt on the voice activity"""
    finsrt = max(srt, key=lambda x: x[1])[1]
    startsrt = min(srt, key=lambda x: x[0])[0]
    lensrt = finsrt - startsrt
    maxstretch = max(length / lensrt, 1.)

    disc_va = discretize_timestamp(voice_activity,
                                   chunk=chunk)

    def fopt(stretch):
        """wrapper for finding the optimal shift"""
        _, coef_correl = opt_shift(stretch, disc_va, srt, chunk=chunk)
        return - coef_correl

    print("Synchronizing...")
    if True:
        stretch = scipy.optimize.minimize_scalar(fopt, bounds=(0.5, maxstretch),
                                                 method='bounded').x

    if False:
        stretch = scipy.optimize.dual_annealing(fopt, bounds=[(0.5, maxstretch)]).x

    if False:
        stretch = scipy.optimize.shgo(fopt, bounds=[(0.5, maxstretch)]).x

    if False:
        stretch = scipy.optimize.basinhopping(fopt, x0=[1.]).x

    if False:
        for s in np.arange(0.6, maxstretch, 0.05):
            stretch = fopt(s)
            print(f"stretching {s:.2f} {1/s:.2f} {stretch:.2f}")

    shift, _ = opt_shift(stretch, disc_va, srt, chunk=chunk)

    return shift, stretch
