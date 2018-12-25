#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Installer for srtsync
"""
from setuptools import setup, find_packages

import srtsync

setup(
        description="Automatic synchronizer of subtitles based on video or other subtitle",
        long_description=open('README.md').read(),
        url='https://github.com/pums974/srtsync',

        author="Alexandre Poux",
        author_email="pums974@gmail.com",

        name='srtsync',
        version=srtsync.__version__,
        packages=find_packages(),

        classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.7",
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Intended Audience :: End Users/Desktop",
            "Natural Language :: English",
            "Operating System :: POSIX :: Linux",
            "Topic :: Multimedia :: Sound/Audio",
            "Topic :: Multimedia :: Video",
            "Topic :: Utilities"
            ],

        install_requires=['pysrt', 'numpy', 'scipy'],
        extras_require={
            'accurate detection of video file': ["pymediainfo"],
            'for voice activity detection (required for sync from video)': ["webrtcvad"],
            },
        python_requires='>=3.6',
        include_package_data=True,

        entry_points={
            'console_scripts': [
                'srtsync = srtsync.main:main',
                ],
            },
        )
