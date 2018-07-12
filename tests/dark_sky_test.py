"""
Testing the DarkSky API connector
"""

import mock
import pytest
from requests.exceptions import HTTPError, InvalidHeader

from tests.test_base import generate_random_key, MockedDarkSkyResponse

from darksky import DarkSky


class TestInitialisation(object):
    """Testing the initialisation of the object with the secret key."""

    def test_init_raises_TypeError_with_no_key_variable(self):
        with pytest.raises(TypeError) as e:
            DarkSky()
        assert "Missing argument. Key is required." in str(e.value)

    # run this next test 30 times
    @pytest.mark.parametrize('exec_no', range(30))
    def test_init_stores_key_variable(self, exec_no):
        key = generate_random_key()
        print("Test {} with key: {}".format(exec_no, key))
        darksky_with_key = DarkSky(key=key)
        assert darksky_with_key.key == key


class TestRequest(object):

    # this is the setup
    @staticmethod
    @pytest.fixture
    def darksky():
        return DarkSky(key=generate_random_key())

    def test_request_raises_TypeError_with_missing_lat_long(self, darksky):
        with pytest.raises(TypeError) as e:
            darksky.request()
        assert ("Missing argument. Latitude and Longitude are required."
                in str(e.value))

    def test_request_raises_TypeError_with_missing_long(self, darksky):
        with pytest.raises(TypeError) as e:
            darksky.request(latitude='1.0')
        assert ("Missing argument. Latitude and Longitude are required."
                in str(e.value))

    def test_request_raises_TypeError_with_missing_lat(self, darksky):
        with pytest.raises(TypeError) as e:
            darksky.request(longitude='1.0')
        assert ("Missing argument. Latitude and Longitude are required."
                in str(e.value))

    @mock.patch('darksky.requests.get')
    def test_response_no_error_when_status_code_ok(self,
                                                   mock_request,
                                                   darksky):
        try:
            mock_request.return_value = MockedDarkSkyResponse(status_code=200)
            darksky.request(latitude='1.0', longitude='1.0')
        except Exception as e:
            pytest.fail(str(e))

    @pytest.mark.parametrize('status_code', range(201, 600))
    @mock.patch('darksky.requests.get')
    def test_response_raises_error_when_status_code_not_ok(self,
                                                           mock_request,
                                                           status_code,
                                                           darksky):
        print(status_code)
        with pytest.raises(HTTPError) as e:
            mock_response = MockedDarkSkyResponse(status_code=status_code)
            mock_request.return_value = mock_response
            darksky.request(latitude='1.0', longitude='1.0')
        assert (str(status_code) in str(e.value))

    @mock.patch('darksky.requests.get')
    def test_response_raises_no_error_when_header_is_json(self,
                                                          mock_request,
                                                          darksky):
        try:
            mock_response = MockedDarkSkyResponse()
            mock_request.return_value = mock_response
            darksky.request(latitude='1.0', longitude='1.0')
        except InvalidHeader as e:
            pytest.fail(str(e))

    @pytest.mark.parametrize('headers', [
                            {'Content-Type': "text/plain; charset=utf-8"},
                            {'Content-Type': 'text/html; charset=ISO-8859-1'}])
    @mock.patch('darksky.requests.get')
    def test_response_raises_error_when_header_not_json(self,
                                                        mock_request,
                                                        headers,
                                                        darksky):
        with pytest.raises(InvalidHeader) as e:
            mock_response = MockedDarkSkyResponse(headers=headers)
            print(headers)
            mock_request.return_value = mock_response
            darksky.request(latitude='1.0', longitude='1.0')
        assert ("Content type is not JSON as expected:" in str(e.value))

    @mock.patch('darksky.requests.get')
    def test_response_raises_error_when_header_is_missing_content_type(
                                                                self,
                                                                mock_request,
                                                                darksky):
        with pytest.raises(InvalidHeader) as e:
            mock_response = MockedDarkSkyResponse(headers={})
            mock_request.return_value = mock_response
            darksky.request(latitude='1.0', longitude='1.0')
        assert "Content-Type not returned in header" in str(e.value)
