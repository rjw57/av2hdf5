#!/usr/bin/env python

import os
import sys

from setuptools import setup

setup(
    name='av2hdf5',
    version='0.1.0',
    description='Convert video files to (compressed) HDF5',
    long_description='',
    author='Rich Wareham',
    author_email='rjw57@cam.ac.uk',
    url='https://github.com/rjw57/av2hdf5',
    packages=[
        'av2hdf5',
    ],
    package_dir={'av2hdf5': 'av2hdf5'},
    setup_requires=['pip'],
    install_requires=[
        'av',
        'docopt',
        'tables',
    ],
    license="BSD",
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'av2hdf5 = av2hdf5:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
