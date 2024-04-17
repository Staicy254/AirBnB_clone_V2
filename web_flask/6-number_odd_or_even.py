#!/usr/bin/python3
"""A Flask web application with multiple routes, data validation, and templating."""

from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def index():
    """The home page, returning a greeting."""
    return "Welcome to the enhanced Flask web application!"


@app.route('/hbnb')
def hbnb():
    """The HBNB specific page, returning a simple message."""
    return "This is the HBNB page!"


@app.route('/c/<text>')
def c_page(text):
    """Dynamic route displaying 'C' followed by the decoded text."""
    return f"C {text.replace('_', ' ')}"


@app.route('/python', defaults={'text': 'is cool'})
@app.route('/python/<text>')
def python_page(text):
    """Dynamic route displaying 'Python' followed by provided or default text."""
    return f"Python {text.replace('_', ' ')}"


@app.route('/number/<int:n>')
def number_page(n):
    """The number page, validating and returning the integer argument."""
    return f"{n} is a number"


@app.route('/number_template/<int:n>')
def number_template(n=None):
    """Displays an HTML page with the provided integer (if valid)."""
    if n is not None:
        return render_template("5-number.html", n=n)  # Assuming a 5-number.html template exists
    return "Please provide a valid integer."


@app.route('/number_odd_or_even/<int:n>')
def number_odd_or_even(n=None):
    """Displays an HTML page indicating if the number is odd or even (if valid)."""
    if n is not None:
        eo = "even" if n % 2 == 0 else "odd"
        return render_template("6-number_odd_or_even.html", n=n, eo=eo)  # Assuming a 6-number_odd_or_even.html template exists
    return "Please provide a valid integer."


if __name__ == '__main__':
    app.run(debug=True)  # Include debug=True for development mode error reporting

