#!/usr/bin/python3
"""Flask web application displaying state and amenity filters."""

from flask import Flask, render_template
from models import storage
from models.amenity import Amenity
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/hbnb_filters')
def hbnb_filters():
    """Hbnb_filters page, retrieving and sorting states and amenities."""
    all_states = list(storage.all(State).values())
    amenities = list(storage.all(Amenity).values())
    all_states.sort(key=lambda x: x.name)
    amenities.sort(key=lambda x: x.name)

    # Sort cities within each state (assuming relevant functionality exists)
    # for state in all_states:
    #     state.cities.sort(key=lambda x: x.name)

    context = {'states': all_states, 'amenities': amenities}
    return render_template('10-hbnb_filters.html', **context)


@app.teardown_appcontext
def teardown(exc):
    """
    The Flask app/request context end event listener, closing the storage.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

