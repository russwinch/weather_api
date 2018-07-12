"""
Request data from DarkSky's weather api.
"""

import json
import requests
from requests.exceptions import HTTPError, InvalidHeader


class DarkSky(object):

    """A DarkSky API client."""

    def __init__(self, key=None):
        """
        :key: the secret api key
        """
        if not key:
            raise TypeError(
                "Missing argument. Key is required.")
        self.key = key

    @staticmethod
    def _raise_http_error(r):
        """
        Attempt to look up the status code from a response
        and raise a HTTPError.

        :r: the response object with the erroneous status code
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
                timeout=2,
                file_out=None):

        """
        Return a response object from the Dark Sky API.

        :latitude and longitude: can be supplied as string or float
        :options: converted into query string paramaters
        :headers: includes http gzip conversion by default
        :timeout: in seconds
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

        if file_out:
            self.write_file(r, file_out)
        return r

    def write_file(self, response, file_out):
        """
        Store a response locally in a file as text.

        :file_out: location of the file where the forecast json will be stored
        """
        try:
            with open(file_out, mode='w') as f_out:
                f_out.write(response.text)
        except Exception as e:
            # determine errors and add here
            # log e
            # raise e
            print(e)
        print("Updated and written to local file.")

    def read_file(self, file_in):
        """
        Return a parsed dict from the local text file.

        :file_in: location of the file with the forecast json
        """
        try:
            with open(file_in) as f_in:
                weather_json = f_in.read()
                weather_dict = json.loads(weather_json)
        except FileNotFoundError as e:
            # log error
            print(e)
        else:
            return weather_dict


if __name__ == '__main__':
    import instance.config

    dark_sky = DarkSky(key=instance.config.DARK_SKY_API_KEY)
    dark_sky.request(latitude=instance.config.LATITUDE,
                     longitude=instance.config.LONGITUDE,
                     file_out=instance.config.WEATHER_FILE)
    weather_dict = dark_sky.read_file(instance.config.WEATHER_FILE)
    try:
        print("Weather summary:\n{}".format(
                                        weather_dict['minutely']['summary']))
    except TypeError as e:
        # log error
        print('Error opening data file')
