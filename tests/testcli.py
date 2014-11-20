import os

from docopt import DocoptExit
from mock import patch
from tempdir import TempDir

# pylint: disable=no-name-in-module
from nose.tools import assert_equal, assert_greater, assert_raises, assert_true
from nose.tools import assert_is_none

from av2hdf5 import main

@patch('sys.argv', ['av2hdf5', '-h'])
@patch('sys.stdout')
def test_h_flag(stdout_mock):
    """Test basic invocation of the CLI with -h"""
    with assert_raises(SystemExit) as cm:
        main()
    assert_is_none(cm.exception.code)
    assert_greater(stdout_mock.write.call_count, 0)

@patch('sys.argv', ['av2hdf5', '--help'])
@patch('sys.stdout')
def test_help_flag(stdout_mock):
    """Test basic invocation of the CLI with --help"""
    with assert_raises(SystemExit) as cm:
        main()
    assert_is_none(cm.exception.code)
    assert_greater(stdout_mock.write.call_count, 0)

@patch('sys.argv', ['av2hdf5'])
def test_no_flags():
    """Test basic invocation of the CLI with no options"""
    assert_raises(DocoptExit, main)

def test_simple_usage():
    """Test basic invocation of the CLI with a sample video clip"""
    video_fn = datafile_path('event-01-view-01-short.mp4')
    with TempDir() as tmp_d:
        out_fn = os.path.join(tmp_d, 'output.h5')
        argv = ['av2hdf5', video_fn, out_fn]
        with patch('sys.argv', argv):
            main()

        # Check output exists and is non-zero size
        assert_true(os.path.exists(out_fn))
        assert_greater(os.stat(out_fn).st_size, 0)

### UTILITY FUNCTIONS ###

def datafile_path(name):
    this_dir = os.path.dirname(__file__)
    data_dir = os.path.join(this_dir, 'data')
    file_path = os.path.join(data_dir, name)
    assert_true(os.path.exists(file_path))
    return file_path
