"""
Some helper functions to manage DarkSky responses and to store and retrieve
them from a text file.

This is a temporary file until there is integration with flask.
"""
import instance.config
import json

from darksky import DarkSky


def read_local_darksky(file_in, print_summary=True):
    """
    Returns a parsed dict from the local text file.

    :file_in: the location of the file with the forecast json
    :print_summary: a boolean which controls if the summary forecast will be
                    printed after retrieval
    """
    with open(file_in) as f:
        weather_json = f.read()
    weather_dict = json.loads(weather_json)
    if print_summary:
        print("Weather summary:\n{}".format(weather_dict['daily']['summary']))

    return weather_dict


def update_darksky(file_out):
    """
    Requests and returns a response from DarkSky using instance config.

    :file_out: the location of the file where the forecast json will be stored
    """
    dark_sky = DarkSky(key=instance.config.DARK_SKY_API_KEY)
    r = dark_sky.request(latitude=instance.config.LATITUDE,
                         longitude=instance.config.LONGITUDE)
    with open(file_out, mode='w') as out:
        out.write(r.text)
    print("Updated and written to local file.")

    return r


if __name__ == '__main__':
    weather_file = 'darksky.json'

    weather_response = update_darksky(weather_file)
    weather_dict = read_local_darksky(weather_file)
