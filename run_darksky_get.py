"""
Some helper functions to manage DarkSky responses and to store and retrieve
them from a text file.

This is a temporary file until there is integration with flask.
"""
import instance.config
import json

from darksky import DarkSky

FILE = 'darksky.json'


def write_file(file_out, data):
    with open(file_out, mode='w') as out:
        out.write(data)


def read_file(file_in):
    """Retrieves and parses the json stored in the file and returns a dict."""
    with open(file_in) as f:
        text = f.read()
    return json.loads(text)


def update_darksky():
    """Requests and returns a response from DarkSky using instance config."""
    dark_sky = DarkSky(key=instance.config.DARK_SKY_API_KEY)
    r = dark_sky.request(latitude=instance.config.LATITUDE,
                         longitude=instance.config.LONGITUDE)
    write_file(FILE, r.text)
    print("Updated and written to local file.")
    return r


def read_local_darksky(print_summary=True):
    """
    Returns a parsed dict from the local text file.
    :print_summary: a boolean which controls if the summary forecast will be
                    printed after retrieval.
    """
    weather_dict = read_file(FILE)
    if print_summary:
        print("Daily summary:\n{}".format(weather_dict['daily']['summary']))
    return weather_dict


if __name__ == '__main__':
    update_darksky()
    read_local_darksky()
