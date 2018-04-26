'''Requests data from the weather api.'''

import requests
from requests.exceptions import InvalidHeader
import instance.config  # modify this once flask is set up *****


def dark_sky_call(
                key=None,
                latitude=None,
                longitude=None,
                options={'units': 'si', 'extend': 'hourly'},
                headers={'Accept-Encoding': 'gzip'},
                timeout=2):
    '''
    Returns a request object from the Dark Sky API.

    key is the secret api key
    latitude and longitude can be supplied as string or float
    options are converted into query string paramaters
    headers includes http gzip conversion by default
    timeout is in seconds
    '''
    if not key or not latitude or not longitude:
        raise TypeError(
            "Missing argument. key, latitude and longitude are all required.")

    call = (
        'https://api.darksky.net/forecast/'
        + instance.config.DARK_SKY_API_KEY + '/'
        + str(latitude) + ','
        + str(longitude))

    return requests.get(call, params=options, headers=headers, timeout=timeout)


if __name__ == '__main__':
    r = dark_sky_call(
            key=instance.config.DARK_SKY_API_KEY,
            latitude=instance.config.LATITUDE,
            longitude=instance.config.LONGITUDE)

    if r.status_code != requests.codes.ok:
        r.raise_for_status()

    content_type = r.headers["Content-Type"]
    if 'application/json' not in content_type:
        raise InvalidHeader(
                "Wrong content type in header: {}".format(content_type))

    print(r.url)
    # print(r.text)
    # print(r.json())  # raises an exception if unable to decode
