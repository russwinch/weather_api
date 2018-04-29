"""
A Flask application to provide an api interface via a secure login page
"""


from flask import Flask


# create the application object:
app = Flask(__name__)


@app.route("/")
def main_page():
    return "Weather API - Main Page"


if __name__ == "__main__":
    app.run(debug=True)
