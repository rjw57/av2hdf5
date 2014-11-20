from docopt import DocoptExit
from mock import patch
from nose.tools import assert_equal, assert_not_equal, assert_greater, assert_raises

from av2hdf5 import main

@patch('sys.argv', ['av2hdf5', '-h'])
@patch('sys.exit')
@patch('sys.stdout')
def test_h_flag(stdout_mock, exit_mock):
    """Test basic invocation of the CLI with -h"""
    main()
    exit_mock.assert_called_with(0)
    assert_greater(stdout_mock.write.call_count, 0)

@patch('sys.argv', ['av2hdf5', '--help'])
@patch('sys.exit')
@patch('sys.stdout')
def test_help_flag(stdout_mock, exit_mock):
    """Test basic invocation of the CLI with --help"""
    main()
    exit_mock.assert_called_with(0)
    assert_greater(stdout_mock.write.call_count, 0)

@patch('sys.argv', ['av2hdf5'])
def test_no_flags():
    """Test basic invocation of the CLI with no options"""
    assert_raises(DocoptExit, main)
