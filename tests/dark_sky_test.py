"""
Testing the DarkSky API connector
"""

import mock
import pytest
import random
import string
import unittest
import requests
from requests.exceptions import HTTPError
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


class MockedResponse(object):
    def __init__(self,
                 content='{}',
                 headers={
                        'Server': 'nginx',
                        'Date': 'Sat, 19 May 2018 13:13:34 GMT',
                        'Content-Type': 'application/json; charset=utf-8',
                        'Transfer-Encoding': 'chunked',
                        'Connection': 'keep-alive',
                        'X-Forecast-API-Calls': '2',
                        'Cache-Control': 'max-age=60',
                        'Expires': 'Sat, 19 May 2018 13:14:34 +0000',
                        'X-Response-Time': '152.328ms',
                        'Content-Encoding': 'gzip'},
                 status_code=200):

        self.status_code = status_code
        self.headers = headers
        self.content = content

    def raise_for_status(self):
        print('Mocked raise_for_status called with status code {}.'.format(
                                                            self.status_code))
        raise HTTPError(self.status_code)


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


def test_response_no_error_when_status_code_ok(darksky):
    try:
        with mock.patch('darksky.requests.get') as mock_request:
            mock_request.return_value = MockedResponse(status_code=200)
            darksky.request(latitude='1.0', longitude='1.0')
    except Exception as e:
        pytest.fail(str(e))


@pytest.mark.parametrize('status_code', range(400, 600))
@mock.patch('darksky.requests.get')
def test_response_raises_error_when_status_code_not_ok(mock_request,
                                                       status_code,
                                                       darksky):
    print(status_code)
    with pytest.raises(HTTPError) as e:
        mock_response = MockedResponse(status_code=status_code)
        mock_request.return_value = mock_response
        req = darksky.request(latitude='1.0', longitude='1.0')

        req.raise_for_status.assert_called_once_with(HTTPError)

        print("Error generated: {} {}".format(e.type, e.value))
        assert (str(status_code) == str(e.value))

# 'text/html; charset=ISO-8859-1'
