#!/usr/bin/python3
"""Start a Flask web application"""

from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Returns a string for /"""
    return 'Hello HBNB!'


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Returns a string for /hbnb"""
    return 'HBNB'


@app.route("/c/<text>", strict_slashes=False)
def ctext(text):
    """Returns a string for /c/<text>"""
    text2 = text.replace('_', ' ')
    return "C %s" % text2


@app.route("/python", defaults={'text': 'is cool'}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_text(text):
    """Returns a string for /python/<text> or /python"""
    text2 = text.replace('_', ' ')
    return "Python %s" % text2


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Returns a string for /number/<n>"""
    if type(n) == int:
        return '%i is a number\n' % n


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
