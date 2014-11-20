"""
Extract frames from video into HDF5 formatted files.

Usage:
    av2hdf5 (-h | --help)
    av2hdf5 <video> <output>

The <video> argument specifies a file containing a FFMPEG-compatible video file
to extract frames from. The <output> argument specifies a HDF5 file to write
output to. If <output> already exists, it will be overwritten.

"""
import logging
import sys

import av
import docopt
import tables
import numpy as np

LOG = logging.getLogger()

def main():
    """Main entry point for tool."""

    # Parse command line options
    opts = docopt.docopt(__doc__)

    # Perform conversion
    convert(opts['<video>'], opts['<output>'])

def convert(video_fn, output_fn):
    """Perform the actual extraction of video frames.

    """
    LOG.info('Opening output: {0}'.format(output_fn))
    out_f = tables.open_file(output_fn, 'w')

    LOG.info('Opening input: {0}'.format(video_fn))
    for frame_idx, frame in enumerate(read_video(video_fn)):
        if frame_idx > 0 and frame_idx % 100 == 99:
            LOG.info('Read {0} frames'.format(frame_idx + 1))

        # Convert frame to numpy array
        frame_array = np.asarray(frame).astype(np.uint8)

        # Create dataset in output
        frame_ds = out_f.create_array(
            '/', 'frame{0:05d}'.format(frame_idx), frame_array
        )

        # Write metadata on frame
        frame_ds.attrs.original_idx = frame_idx
    LOG.info('Read {0} frame(s) in total'.format(frame_idx + 1))

def read_video(fn):
    """Takes a path to a video file. Return a generator which will generator a
    PIL image for each video frame,

    """
    LOG.info('Opening video file: {0}'.format(fn))
    container = av.open(fn)
    stream = next(s for s in container.streams if s.type == 'video')
    for packet in container.demux(stream):
        for frame in packet.decode():
            yield frame.reformat(frame.width, frame.height, 'rgb24').to_image()
