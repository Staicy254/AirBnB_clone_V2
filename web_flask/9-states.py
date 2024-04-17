#!/usr/bin/python3
"""
Flask web application displaying states and their sorted cities.
"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states')
@app.route('/states/<id>')
def states(id=None):
    """
    The states page, handling both state list and individual state views.
    """
    all_states = list(storage.all(State).values())
    state = None
    case = None

    # Handle state list view
    if id is None:
        states = all_states
        for state in states:
            state.cities.sort(key=lambda x: x.name)
        states.sort(key=lambda x: x.name)
        case = 1  # Indicate state list view

    # Handle individual state view with error handling
    else:
        try:
            state = storage.get(State, id)
            if state is None:
                raise Exception("State not found")  # Raise custom exception
            state.cities.sort(key=lambda x: x.name)
            case = 2  # Indicate individual state view
        except Exception as e:
            case = 404  # Handle state not found case

    context = {'states': states, 'state': state, 'case': case}
    return render_template('9-states.html', **context)


@app.teardown_appcontext
def teardown(exc):
    """
    The Flask app/request context end event listener, closing the storage.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

