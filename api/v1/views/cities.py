#!/usr/bin/python3
"""Instance of Flask"""


from flask import Flask, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False)
def get_city_from_state_by_id(state_id):
    """Gets city from a state."""
    get_state = storage.get(State, state_id)
    if get_state is None:
        abort(404)
    cities = [city.to_dict() for city in get_state.cities]
    return (jsonify(cities), 200)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def get_city_by_id(city_id=None):
    """Gets a city base form the id."""
    get_city = storage.get(City, city_id)
    if get_city is None:
        abort(404)
    else:
        return (jsonify(get_city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """Deletes a city base form the id."""
    data_id = storage.get(City, city_id)
    if data_id is None:
        abort(404)
    else:
        storage.delete(data_id)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_a_city(state_id):
    """ Create a new city in a state by id."""
    state_data = storage.get('State', state_id)
    if state_data is None:
        abort(404)
    is_json = request.get_json(silent=True)
    if not is_json:
        abort(400, "Not a JSON")
    if "name" not in is_json.keys():
        abort(400, "Missing name")
    is_json['state_id'] = state_data.id
    new_city = City(**is_json)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """ Update a old city."""
    first_city = storage.get('City', city_id)
    if first_city is None:
        abort(404)
    is_json = request.get_json()
    if is_json is None:
        abort(400, "Not a JSON")
    for key, value in is_json.items():
        setattr(first_city, key, value)
    storage.save()
    return jsonify(first_city.to_dict()), 200
