"""Manages the collection of a DarkSky response."""
import instance.config
import json

from darksky import DarkSky

FILE = 'darksky.json'


def write_file(file_out, data):
    with open(file_out, mode='w') as out:
        out.write(data)


def read_file(file_in):
    with open(file_in) as f:
        data = f.read()
    return json.loads(data)


def update_darksky():
    dark_sky = DarkSky(key=instance.config.DARK_SKY_API_KEY)
    r = dark_sky.request(latitude=instance.config.LATITUDE,
                         longitude=instance.config.LONGITUDE)
    write_file(FILE, r.text)
    print("Updated and written to local file.")


def read_local_darksky(print_summary=True):
    js = read_file(FILE)
    if print_summary:
        print("Daily summary:\n{}".format(js['daily']['summary']))


if __name__ == '__main__':
    update_darksky()
    read_local_darksky()
