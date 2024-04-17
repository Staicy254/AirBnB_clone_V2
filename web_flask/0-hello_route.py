#!/usr/bin/python3
"""Minimal Flask web - applicationerror handling."""

from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def index():
    """Home page, rendered with a template."""
    return render_template('index.html')  # Assuming an 'index.html' template exists


@app.errorhandler(404)
def not_found(error):
    """Custom error handler - 404 Not Found."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

