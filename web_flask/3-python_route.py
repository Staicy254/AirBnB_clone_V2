#!/usr/bin/python3
"""Flask web application with multiple routes & dynamic content."""

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def index():
    """Home page, returning a greeting."""
    return "Welcome to the HBNB web application!"


@app.route('/hbnb')
def hbnb():
    """HBNB specific page, returning a simple message."""
    return "This is the HBNB page!"


@app.route('/c/<text>')
def c_page(text):
    """Dynamic route displaying 'C' followed by the decoded text."""
    return f"C {text.replace('_', ' ')}"


@app.route('/python', defaults={'text': 'is cool'})
@app.route('/python/<text>')
def python_page(text):
    """
    Dynamic route displayin 'Python' - provided or default text.
    """
    return f"Python {text.replace('_', ' ')}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

