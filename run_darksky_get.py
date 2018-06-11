"""
Some helper functions to manage DarkSky responses and to store and retrieve
them from a text file.

This is a temporary file until there is integration with flask.
"""
import instance.config
import json

from darksky import DarkSky


def read_local_darksky(file_in):
    """
    Returns a parsed dict from the local text file.

    :file_in: the location of the file with the forecast json
    """
    with open(file_in) as f_in:
        weather_json = f_in.read()

    weather_dict = json.loads(weather_json)
    return weather_dict


def update_darksky(file_out):
    """
    Requests and returns a response from DarkSky using instance config,
    storing it locally in a file as text.

    :file_out: the location of the file where the forecast json will be stored
    """
    dark_sky = DarkSky(key=instance.config.DARK_SKY_API_KEY)
    response = dark_sky.request(latitude=instance.config.LATITUDE,
                                longitude=instance.config.LONGITUDE)

    with open(file_out, mode='w') as f_out:
        f_out.write(response.text)

    print("Updated and written to local file.")
    return response


if __name__ == '__main__':
    weather_file = 'darkskyacs.json'  # this should move to the config

    # weather_response = update_darksky(weather_file)
    weather_dict = read_local_darksky(weather_file)
    print("Weather summary:\n{}".format(weather_dict['minutely']['summary']))
