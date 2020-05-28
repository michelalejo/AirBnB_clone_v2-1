#!/usr/bin/python3
"""Instance of Flask"""


from flask import Flask, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state_state():
    """Gets all states"""
    new_dict = []
    for data in storage.all(State).values():
        new_dict.append(data.to_dict())
    return jsonify(new_dict)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id=None):
    """Gets a state base form the id."""
    data_id = storage.get(State, state_id)
    if data_id is None:
        abort(404)
    else:
        return jsonify(data_id.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id=None):
    """Deletes a state base form the id."""
    data_id = storage.get(State, state_id)
    if data_id is None:
        abort(404)
    else:
        storage.delete(data_id)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_a_state():
    """ Create a new state."""
    is_json = request.get_json(silent=True)
    if not is_json:
        abort(400, "Not a JSON")
    if "name" not in is_json.keys():
        abort(400, "Missing name")
    new_state = State(**is_json)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_a_state(state_id):
    """ Update a old state."""
    first_state = storage.get(State, state_id)
    if first_state is None:
        abort(404)
    is_json = request.get_json()
    dont = ['id', 'created_at', 'updated_at']
    if is_json is None:
        abort(400, "Not a JSON")
    for key, value in is_json.items():
        if key in dont:
            pass
        else:
            setattr(first_state, key, value)
    storage.save()
    return jsonify(first_state.to_dict()), 200
