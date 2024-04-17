#!/usr/bin/python3
"""
Flask web application displaying HBnB properties with filters.
"""

from flask import Flask, render_template, Markup
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/hbnb')
def hbnb():
    """Hbnb page, retrieving and sorting states, amenities, and places."""
    all_states = list(storage.all(State).values())
    amenities = list(storage.all(Amenity).values())
    places = list(storage.all(Place).values())
    all_states.sort(key=lambda x: x.name)
    amenities.sort(key=lambda x: x.name)
    places.sort(key=lambda x: x.name)

    # Sort cities within each state (assuming relevant functionality exists)
    # for state in all_states:
    #     state.cities.sort(key=lambda x: x.name)

    # Apply Markup for safe rendering of user-generated content
    for place in places:
        place.description = Markup(place.description)

    context = {'states': all_states, 'amenities': amenities, 'places': places}
    return render_template('100-hbnb.html', **context)


@app.teardown_appcontext
def teardown(exc):
    """
    The Flask app/request context end event listener, closing the storage.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

