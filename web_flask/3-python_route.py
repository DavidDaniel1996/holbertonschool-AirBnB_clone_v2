#!/usr/bin/python3
""" Script that starts a Flask Web Application """

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def startup():
    """ Displays message on / route """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    """ Displays message on /hbnb route """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """ Displays message on /c/ route """
    text = text.replace('_', " ")
    return 'C {}'.format(text)


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text="is cool"):
    """ Display message on /python/ route"""
    text = text.replace('_', " ")
    return 'Python {}'.format(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
