"""
Testing the DarkSky API connector
"""

import mock
import pytest
import random
import requests
import string
import unittest
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
    assert ("Missing argument. Latitude and longitude are required."
            in str(e.value))


def test_request_raises_TypeError_with_missing_long(darksky):
    with pytest.raises(TypeError) as e:
        darksky.request(latitude='1.0')
    assert ("Missing argument. Latitude and longitude are required."
            in str(e.value))


def test_request_raises_TypeError_with_missing_lat(darksky):
    with pytest.raises(TypeError) as e:
        darksky.request(longitude='1.0')
    assert ("Missing argument. Latitude and longitude are required."
            in str(e.value))


if __name__ == '__main__':
    unittest.main()
