"""
Requests data from the weather api.

"""

import requests
from requests.exceptions import InvalidHeader

import instance.config  # modify this once flask is set up *****


class DarkSky(object):

    """A DarkSky API client."""

    def __init__(self, key=None):
        """
        :key is the secret api key
        """
        self.key = key

    def request(self,
                latitude=None,
                longitude=None,
                options={'units': 'si', 'extend': 'hourly'},
                headers={'Accept-Encoding': 'gzip'},
                timeout=2):

        """
        Returns a request object from the Dark Sky API.

        :latitude and longitude can be supplied as string or float
        :options are converted into query string paramaters
        :headers includes http gzip conversion by default
        :timeout is in seconds
        """

        if not self.key or not latitude or not longitude:
            raise TypeError(
                "Missing argument. key, latitude and longitude are required.")

        url = ("https://api.darksky.net/forecast/{key}/{lat},{lon}".format(
                   key=instance.config.DARK_SKY_API_KEY,
                   lat=latitude,
                   lon=longitude))

        r = requests.get(url,
                         params=options,
                         headers=headers,
                         timeout=timeout)

        if r.status_code != requests.codes.ok:
            r.raise_for_status()

        content_type = r.headers["Content-Type"]
        if 'application/json' not in content_type:
            raise InvalidHeader(
                    "Content type is not JSON as expected: {}".format(
                        content_type))

        return r


if __name__ == '__main__':
    dark_sky = DarkSky(key=instance.config.DARK_SKY_API_KEY)
    try:
        r = dark_sky.request(latitude=instance.config.LATITUDE,
                             longitude=instance.config.LONGITUDE)
        print(r.json())  # raises an exception if unable to decode

    except ValueError as e:
        print("Decoding failed: {}".format(e))

    except Exception as e:
        print("Error {} occurred. Retry when properly implemented".format(e))
