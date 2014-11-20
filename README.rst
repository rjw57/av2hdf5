av2hdf5: extract video frames into HDF5 container
=================================================

.. image:: https://travis-ci.org/rjw57/av2hdf5.svg?branch=master
    :target: https://travis-ci.org/rjw57/av2hdf5
    :alt: Build status

av2hdf5 is small utility which can pull video frames out of any
FFMPEG-compatible video format and insert them as separate datasets within an
HDF5 file. Each frame may be stored uncompressed or as a one-dimensional array
of bytes representing the JPEG or PNG encoding.

This utility is probably of use to those performing batch scientific computing
on images with software which expects HDF5-formatted input.

License
-------

This utility is © Copyright 2014, Rich Wareham.

See the `LICENSE.txt <LICENSE.txt>`_ file shipped with this repository for more
information.
