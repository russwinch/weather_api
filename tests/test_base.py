"""
Helper functions for use in other tests.
"""

import os
import random
import string


def generate_random_key(length=32):
    key = []
    strings = string.ascii_letters + string.digits
    for l in range(length):
        next_letter = random.choice(strings)
        key.append(next_letter)
    key = ''.join(key)
    print("Generated key length {}: {}".format(length, key))
    return key


class MockedDarkSkyResponse(object):
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
                 status_code=200,
                 text='{}',
                 url='https://api.darksky.net/forecast/...'):

        self.content = content
        self.headers = headers
        self.status_code = status_code
        self.text = text
        self.url = url

        print("Mock created")


def retrieve_test_data(location):
    """
    Reads and returns data from a file.

    :location: is the path to the file
    """
    with open(location) as f:
        return f.read()


def check_files(location):
    """
    Checks and returns True if file exists.

    :location: is the path to the file
    """
    if os.access(location, os.F_OK):
        return True
    return False
