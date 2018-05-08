"""
A Flask application to provide the weather api interface via a secure
login page
"""


from flask import Flask, flash, render_template, redirect, request,\
                  url_for, session


# create the application object:
app = Flask(__name__)

app.secret_key = "my_precious" # this key must be relocated to instance/config


# use decorators to link the function to a url:
@app.route('/')
def home():
    """calls the web site home page"""
    return render_template("index.html")


#  route for handling the login page logic:
@app.route('/login', methods=["GET", "POST"])
def login():
    """calls the web site login page"""
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You are logged in!')
            return redirect(url_for('welcome'))
    return render_template('login.html', error=error)


@app.route('/welcome')
def welcome():
    """calls the web site welcome page"""
    return render_template('welcome.html')


@app.route('/logout')
def logout():
    """calls  the logout logic"""
    session.pop('logged_in', None)
    flash('You were logged out!')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
