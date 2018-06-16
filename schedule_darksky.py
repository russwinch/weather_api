from threading import Thread
import time

from flask import Flask
from requests.exceptions import ReadTimeout, ConnectionError
import schedule

from darksky import DarkSky
import instance.config as config


app = Flask(__name__)


def update_weather(weather_file):
    try:
        dark_sky.request(latitude=config.latitude,
                         longitude=config.longitude,
                         file_out=config.weather_file)
    except (ConnectionError, ReadTimeout) as e:
        print(e)
        # log this


def create_schedule(job, *args, interval=15, units='minutes', **kwargs):
    sched = getattr(schedule.every(interval), units)
    sched.do(job, *args, **kwargs)


def threaded_schedule_run():
    while True:
        schedule.run_pending()
        time.sleep(1)


@app.route("/")
def weather():
    weather_dict = dark_sky.read_file(config.weather_file)
    w = weather_dict['minutely']['summary']
    t = weather_dict['currently']['time']
    print("Weather summary:\n{}".format(w))
    return f"Weather at {t} is like: {w}"


if __name__ == '__main__':
    dark_sky = DarkSky(key=config.dark_sky_api_key)

    create_schedule(update_weather,
                    config.weather_file,
                    interval=config.darksky_interval,
                    units='seconds')  # for test purposes
    s = Thread(target=schedule.run_all())
    s.start()
    t = Thread(target=threaded_schedule_run)
    t.start()

    app.run(debug=True, use_reloader=False)
