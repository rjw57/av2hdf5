"""
Extract frames from video into HDF5 formatted files.

Usage:
    av2hdf5 (-h | --help)
    av2hdf5 [options]
        [--start=FRAME] [--duration=COUNT]
        [--jpeg | --png | --raw] <video> <output>

General options:
    -h, --help              Show a brief usage summary.
    -v, --verbose           Increase logging verbosity.

Video decoding options:
    -s, --start=FRAME       Start decoding from 0-indexed frame index FRAME.
    -t, --duration=COUNT    Decode only COUNT frames from the input.

Encoding options:
    --jpeg                  Write output as a JPEG-encoded byte stream.
    --png                   Write output as a PNG-encoded byte stream.
    --raw                   Write output as raw 8-bit pixel values. (default)

The <video> argument specifies a file containing a FFMPEG-compatible video file
to extract frames from. The <output> argument specifies a HDF5 file to write
output to. If <output> already exists, it will be overwritten.

The HDF5 file will be created with a number of datasets under the root node.
Each dataset will have the following attributes:

    * original_idx: the 0-based index into the orinal file of this frame
    * content_id: a unique ID string for the frame based on its content
    * encoded_id: a unique ID string for the frame based on its encoding
    * encoding: one of 'raw', 'jpeg', 'png' specifying the encoding

If encoding is 'raw' then the frame is stored as an uncompressed NxMx3 array.
For other encodings, the frame is stored as a one-dimensional array of bytes
representing the encoded frame.

The content_id attribute is independent of the encoding used for the frame and
represents a unique id for the *content* of the frame independent of encoding
artefacts. The encoding_id represents a unique id for a particular encoding of
the frame. Corresponding frames in a HDF5 file using the jpeg, raw and png
encodings will have identical content_id attributes but distinct encoded_id
attributes.

"""
import enum
import hashlib
import io
import logging
import sys

import av
import docopt
import tables
import numpy as np

LOG = logging.getLogger()

# pylint: disable=too-few-public-methods
class Encoding(enum.Enum):
    raw = 'raw'
    jpeg = 'jpeg'
    png = 'png'

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

    if opts['--jpeg']:
        encoding = Encoding.jpeg
    elif opts['--png']:
        encoding = Encoding.png
    else:
        encoding = Encoding.raw

    # Perform conversion
    convert(frames, output, encoding=encoding)

def int_or_default(v, default=None):
    """Return v as an integer or return *default* is *v* is None."""
    if v is None:
        return default
    return int(v)

def convert(frames, output, encoding=Encoding.raw):
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

        # Hash data to give frame "id"
        hashfunc = hashlib.sha1()
        hashfunc.update(frame_array.tobytes())
        frame_id = hashfunc.hexdigest()

        if encoding is Encoding.raw:
            # Leave as is
            pass
        elif encoding is Encoding.jpeg:
            fp = io.BytesIO()
            frame.save(fp, format='jpeg', quality=100)
            frame_array = np.frombuffer(fp.getvalue(), np.uint8)
        elif encoding is Encoding.png:
            fp = io.BytesIO()
            frame.save(fp, format='png')
            frame_array = np.frombuffer(fp.getvalue(), np.uint8)
        else:
            assert False

        # Create dataset in output
        frame_ds = output.create_array(
            '/', 'frame{0:05d}'.format(frame_idx), frame_array
        )

        # Hash encoded data to give encoded if
        hashfunc = hashlib.sha1()
        hashfunc.update(frame_array.tobytes())
        frame_enc_id = hashfunc.hexdigest()

        # Write metadata on frame
        frame_ds.attrs.original_idx = frame_idx
        frame_ds.attrs.encoding = encoding.value
        frame_ds.attrs.content_id = frame_id
        frame_ds.attrs.encoded_id = frame_enc_id

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
