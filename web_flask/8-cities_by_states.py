#!/usr/bin/python3
"""A Flask web application displaying states and their sorted cities."""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/cities_by_states')
def cities_by_states():
    """The cities_by_states page, retrieving and sorting states and cities."""
    all_states = list(storage.all(State).values())
    all_states.sort(key=lambda x: x.name)  # Sort states by name

    # Sort cities within each state
    for state in all_states:
        state.cities.sort(key=lambda x: x.name)

    context = {'states': all_states}
    return render_template('8-cities_by_states.html', **context)


@app.teardown_appcontext
def teardown(exc):
    """The Flask app/request context end event listener, closing the storage."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

