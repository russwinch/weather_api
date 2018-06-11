from threading import Thread
import time

from flask import Flask
from requests.exceptions import ReadTimeout
import schedule

from run_darksky_get import update_darksky, read_local_darksky


app = Flask(__name__)


def update_weather(weather_file):
    try:
        update_darksky(weather_file)
    except ReadTimeout as e:
        # change the retry interval
        print(e)
        raise e
        pass


def create_schedule(job, *args, interval=15, units='minutes', **kwargs):
    sched = getattr(schedule.every(interval), units)
    s = sched.do(update_weather, weather_file)
    return s


def threaded():
    while True:
        schedule.run_pending()
        time.sleep(1)


@app.route("/")
def weather():
    weather_dict = read_local_darksky(weather_file)
    w = weather_dict['minutely']['summary']
    t = weather_dict['currently']['time']
    print("Weather summary:\n{}".format(w))
    return f"Weather at {t} is like: {w}"


if __name__ == '__main__':
    weather_file = 'darksky.json'  # this should move to the config
    update_interval = 1  # this should move to the config
    update_error_interval = 1  # this should move to the config

    create_schedule(update_weather,
                    weather_file,
                    interval=update_interval)
                    # units='seconds')
    schedule.run_all()  # remove this or trigger another way. shouldn't block flask from starting up
    t = Thread(target=threaded)
    t.start()

    app.run(debug=True, use_reloader=False)
