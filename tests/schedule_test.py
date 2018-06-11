
"""
Testing the scheduling
"""

import mock
import pytest
from requests.exceptions import HTTPError, InvalidHeader

from tests.test_base import generate_random_key, MockedDarkSkyResponse

class TestErrors(object):


    def test_retry(self):
        pass
