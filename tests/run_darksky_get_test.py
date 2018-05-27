"""
Testing the run_darksky_get.py helpers to read and write files.

There is no error checking within either function
"""
import json
import os
import pytest

import run_darksky_get as ds

OUT_FILE = 'TEST-OUT-FILE.json'
TEST_DATA = 'tests/TEST-DATA-darksky.json'


def _retrieve_test_data(location):
    with open(location) as f:
        return f.read()


def _check_files(OUT_FILE):
    '''Checks files are valid and returns True if output file exists.'''
    if os.access(OUT_FILE, os.F_OK):
        return True
    return False


@pytest.fixture
def test_data():
    # make sure test file is deleted
    yield test_data
    print("teardown")
    if _check_files(OUT_FILE):
        print("removing {}".format(OUT_FILE))
        os.remove(OUT_FILE)


def test_write_file(test_data):
    data = _retrieve_test_data(TEST_DATA)
    ds.write_file(OUT_FILE, str(data))
    written_data = _retrieve_test_data(OUT_FILE)
    assert written_data == data


def test_read_file():
    test_read = ds.read_file(TEST_DATA)
    control_read = _retrieve_test_data(TEST_DATA)
    control_read = json.loads(control_read)
    assert test_read == control_read
