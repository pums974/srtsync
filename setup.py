#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Installer for srtsync
"""
from setuptools import setup, find_packages

import srtsync

setup(
        description="Automatic synchronizer of subtitles based on voice activity in the video",
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

        install_requires=['pysrt', 'numpy', 'scipy', 'webrtcvad'],
        python_requires='>=3.6',
        include_package_data=True,

        # C'est un système de plugin, mais on s'en sert presque exclusivement
        # Pour créer des commandes, comme "django-admin".
        # Par exemple, si on veut créer la fabuleuse commande "proclame-sm", on
        # va faire pointer ce nom vers la fonction proclamer(). La commande sera
        # créé automatiquement.
        # La syntaxe est "nom-de-commande-a-creer = package.module:fonction".
        entry_points={
            'console_scripts': [
                'srtsync = srtsync.main:main',
                ],
            },
        )
