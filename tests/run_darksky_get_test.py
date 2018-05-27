"""
Testing the run_darksky_get.py helpers to read and write files.

There is no error checking within either function so this is not tested.
"""
import json
import mock
import os
import pytest

from tests.test_base import MockedDarkSkyResponse
from tests.test_base import retrieve_test_data, check_files

import run_darksky_get as ds

OUT_FILE = 'TEST-OUT-FILE.json'
TEST_DATA = 'tests/TEST-DATA-darksky.json'


@pytest.fixture
def test_data():
    # make sure test file is deleted
    yield test_data
    print("teardown")
    if check_files(OUT_FILE):
        print("removing {}".format(OUT_FILE))
        os.remove(OUT_FILE)


@mock.patch('darksky.requests.get')
def test_update_darksky(mock_request, test_data):
    test_content = retrieve_test_data(TEST_DATA)
    mock_request.return_value = MockedDarkSkyResponse(text=test_content)
    ds.update_darksky(OUT_FILE)
    written_data = retrieve_test_data(OUT_FILE)

    assert written_data == test_content


def test_read_local_darksky():
    test_read = ds.read_local_darksky(TEST_DATA)
    control_read = retrieve_test_data(TEST_DATA)
    control_read = json.loads(control_read)

    assert test_read == control_read
