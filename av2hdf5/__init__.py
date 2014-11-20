"""
Extract frames from video into HDF5 formatted files.

Usage:
    av2hdf5 (-h | --help)
"""

import sys

import docopt

def main():
    """Main entry point for tool."""

    # Parse command line options
    opts = docopt.docopt(__doc__)

    # Exit signalling success
    sys.exit(0)
