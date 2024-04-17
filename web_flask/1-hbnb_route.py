#!/usr/bin/python3
"""Basic Flask web application -- multiple routes."""

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/')
def index():
    """Home page, returning greeting."""
    return "Welcome to the HBNB web application!"

@app.route('/hbnb')
def hbnb():
    """The HBNB specific page, returning a simple message."""
    return "This is the HBNB page!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

