"""
A Flask application to provide the weather api interface via a secure
login page
"""


from flask import Flask, render_template


# create the application object:
app = Flask(__name__)


# use decorators to link the function to a url:
@app.route("/")
def main_page():
    """calls the web site home page"""
    return render_template("index.html")


#  route for handling the login page logic:
@app.route("/login", methods=["GET", "POST"])
def login_page():
    """calls the web site login page"""
    # authentication to be added:
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
