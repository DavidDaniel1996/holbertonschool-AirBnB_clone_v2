#!/usr/bin/python3
""" Script that starts a Flask Web Application """

from flask import Flask, render_template

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


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """ Displaye message on /number/ route """
    if type(n) == int:
        return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template_route(n):
    """ Diplay html template on /number_template/ route """
    if type(n) == int:
        return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def odd_or_even(n):
    """ Display html template on /number_odd_or_even/ route """
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    if type(n) == int:
        return render_template('6-number_odd_or_even.html', number=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
