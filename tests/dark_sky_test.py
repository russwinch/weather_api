"""
Testing the DarkSky API connector
"""

import mock
import pytest
import random
import string
import unittest
# from unittest.mock import Mock, patch

from darksky import DarkSky


def _generate_random_key(length=32):
    key = []
    strings = string.ascii_letters + string.digits
    for l in range(length):
        next_letter = random.choice(strings)
        key.append(next_letter)
    key = ''.join(key)
    print("Generated key length {}: {}".format(length, key))
    return key


def _mock_response(raise_for_status=None,
                   status_code=200,
                   content_type='application/json; charset=utf-8',
                   content='{}'):
    mock_resp = mock.Mock()
    mock_resp.raise_for_status = mock.Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    mock_resp.status_code = status_code
    # mock_resp.add_header("Content-Type", content_type)

    return mock_resp


def test_init_raises_TypeError_with_no_key_variable():
    with pytest.raises(TypeError) as e:
        DarkSky()
    assert "Missing argument. Key is required." in str(e.value)


# run this next test 30 times
@pytest.mark.parametrize('exec_no', range(30))
def test_init_stores_key_variable(exec_no):
    key = _generate_random_key()
    print("Test {} with key: {}".format(exec_no, key))
    darksky_with_key = DarkSky(key=key)
    assert darksky_with_key.key == key


@pytest.fixture
def darksky():
    return DarkSky(key=_generate_random_key())


def test_request_raises_TypeError_with_missing_lat_long(darksky):
    with pytest.raises(TypeError) as e:
        darksky.request()
    assert ("Missing argument. Latitude and Longitude are required."
            in str(e.value))


def test_request_raises_TypeError_with_missing_long(darksky):
    with pytest.raises(TypeError) as e:
        darksky.request(latitude='1.0')
    assert ("Missing argument. Latitude and Longitude are required."
            in str(e.value))


def test_request_raises_TypeError_with_missing_lat(darksky):
    with pytest.raises(TypeError) as e:
        darksky.request(longitude='1.0')
    assert ("Missing argument. Latitude and Longitude are required."
            in str(e.value))


def test_response_status_code(darksky):
    with mock.patch('dark_sky_test.requests.get') as mock_get:
        mock_resp = _mock_response(status_code=200)
        mock_get.return_value = mock_resp
        result = darksky.request(latitude='1.0', longitude='1.0')
        assert result.status_code == 100
