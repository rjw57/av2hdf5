"""
Extract frames from video into HDF5 formatted files.

Usage:
    av2hdf5 (-h | --help)
    av2hdf5 [options] [--start=FRAME] [--duration=COUNT] <video> <output>

General options:
    -h, --help              Show a brief usage summary.
    -v, --verbose           Increase logging verbosity.

Video decoding options:
    -s, --start=FRAME       Start decoding from 0-indexed frame index FRAME.
    -t, --duration=COUNT    Decode only COUNT frames from the input.

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
    logging.basicConfig(
        level=logging.INFO if opts['--verbose'] else logging.WARN
    )

    # Open input and output
    LOG.info('Opening video input: {0}'.format(opts['<video>']))
    frames = read_video(
        opts['<video>'], start_frame=int_or_default(opts['--start']),
        duration=int_or_default(opts['--duration'])
    )

    LOG.info('Opening HDF5 output: {0}'.format(opts['<output>']))
    output = tables.open_file(opts['<output>'], 'w')

    # Perform conversion
    convert(frames, output)

def int_or_default(v, default=None):
    """Return v as an integer or return *default* is *v* is None."""
    if v is None:
        return default
    return int(v)

def convert(frames, output):
    """Perform the actual extraction of video frames.

    *frames* is an iterable which yields frame index, PIL image pairs for each
    frame.

    *output* is a tables File object to which data should be written.

    """
    for frame_idx, frame in frames:
        if frame_idx > 0 and frame_idx % 100 == 0:
            LOG.info('Read frame {0}'.format(frame_idx))

        # Convert frame to numpy array
        frame_array = np.asarray(frame).astype(np.uint8)

        # Create dataset in output
        frame_ds = output.create_array(
            '/', 'frame{0:05d}'.format(frame_idx), frame_array
        )

        # Write metadata on frame
        frame_ds.attrs.original_idx = frame_idx

def read_video(fn, start_frame=None, duration=None):
    """Takes a path to a video file. Return a generator which will generator a
    PIL image for each video frame.

    If start_frame is not None, an attempt is made to seek to that (0-indexed)
    frame.

    If duration is not None, yield at most that many frames.

    """
    LOG.info('Opening video file: {0}'.format(fn))
    container = av.open(fn)
    n_frames_yielded = 0
    frame_idx = 0 if start_frame is None else start_frame
    container.seek(frame_idx, 'frame')
    stream = next(s for s in container.streams if s.type == 'video')
    for packet in container.demux(stream):
        for frame in packet.decode():
            if duration is not None and n_frames_yielded >= duration:
                return

            # Re-format frame
            frame = frame.reformat(frame.width, frame.height, 'rgb24')

            # Yield frame and frame index
            yield frame_idx, frame.to_image()

            frame_idx += 1
            n_frames_yielded += 1
