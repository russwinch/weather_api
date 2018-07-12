"""
Requests data from the weather api.

"""

import requests
from requests.exceptions import HTTPError, InvalidHeader


class DarkSky(object):

    """A DarkSky API client."""

    def __init__(self, key=None):
        """
        :key is the secret api key
        """
        if not key:
            raise TypeError(
                "Missing argument. Key is required.")
        self.key = key

    @staticmethod
    def _raise_http_error(r):
        """
        Attempts to look up the status code from a response
        and raises a HTTPError.

        :r is the response object
        """
        try:
            # look up the list of codes within requests
            error_desc = requests.status_codes._codes[r.status_code][0]
        except KeyError:
            error_desc = 'Error'

        raise HTTPError("HTTPError: {} Error: {} for url: {}".format(
                                                                r.status_code,
                                                                error_desc,
                                                                r.url))

    def request(self,
                latitude=None,
                longitude=None,
                options={'units': 'si', 'extend': 'hourly'},
                headers={'Accept-Encoding': 'gzip'},
                timeout=2):

        """
        Returns a response object from the Dark Sky API.

        :latitude and longitude can be supplied as string or float
        :options are converted into query string paramaters
        :headers includes http gzip conversion by default
        :timeout is in seconds
        """

        if not latitude or not longitude:
            raise TypeError(
                "Missing argument. Latitude and Longitude are required.")

        url = ("https://api.darksky.net/forecast/{key}/{lat},{lon}".format(
                   key=self.key,
                   lat=latitude,
                   lon=longitude))

        r = requests.get(url=url,
                         params=options,
                         headers=headers,
                         timeout=timeout)

        if r.status_code != requests.codes.ok:
            self._raise_http_error(r)

        try:
            content_type = r.headers["Content-Type"]
        except KeyError:
            raise InvalidHeader("Content-Type not returned in header")

        if 'application/json' not in content_type:
            raise InvalidHeader(
                    "Content type is not JSON as expected: {}".format(
                        content_type))
        return r


if __name__ == '__main__':
    import instance.config  # modify this once flask is set up *****

    dark_sky = DarkSky(key=instance.config.DARK_SKY_API_KEY)
    try:
        r = dark_sky.request(latitude=instance.config.LATITUDE,
                             longitude=instance.config.LONGITUDE)
        print(r.json())  # raises an exception if unable to decode

    except ValueError as e:
        print("Decoding failed: {}".format(e))

    except Exception as e:
        print("Error {} occurred. Retry when properly implemented".format(e))
