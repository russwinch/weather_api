"""
Scheduling of weather updates with threading.

When integrating into the main app the flask parts will be redundant and can be
removed, but this serves as a proof of concept that flask will serve a page
while the schedule is running, without blocking the main thread.
"""
from threading import Thread
import time

from flask import Flask
from requests.exceptions import ReadTimeout, ConnectionError
import schedule

from darksky import DarkSky
import instance.config as config


app = Flask(__name__)


def update_weather(weather_file):
    """
    Request from the DarkSky api and write the response to a text file.

    :weather_file: location of the text file where the response is to be stored
    """
    try:
        dark_sky.request(latitude=config.latitude,
                         longitude=config.longitude,
                         file_out=weather_file)
    except (ConnectionError, ReadTimeout) as e:
        print(e)
        # log this


def create_schedule(job, *args, interval=15, units='minutes', **kwargs):
    """
    Create a scheduled job and pass args and kwargs to it.

    :job: function to be scheduled
    :interval: time interval
    :units: unit of time
    """
    sched = getattr(schedule.every(interval), units)
    sched.do(job, *args, **kwargs)


def threaded_schedule_run():
    """
    Keep checking for the schedule to be due and run it.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)


@app.route("/")
def weather():
    """
    Test route to ensure flask will serve pages with the schedule running.
    """
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
                    units='seconds')  # for test purposes only

    # run the update now in it's own thread
    s = Thread(target=schedule.run_all())
    s.start()
    # thread the check for subsequent updates
    t = Thread(target=threaded_schedule_run)
    t.start()

    app.run(debug=True, use_reloader=False)
