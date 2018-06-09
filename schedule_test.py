from threading import Thread
import time

from flask import Flask
import schedule

from run_darksky_get import update_darksky, read_local_darksky

CURRENT_WEATHER = "not set"

app = Flask(__name__)


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

    # TODO: add wrapper to catch errors, reschedule etc
    s = schedule.every(15).seconds.do(update_darksky, weather_file)
    t = Thread(target=threaded)
    t.start()

    app.run(debug=True, use_reloader=False)
