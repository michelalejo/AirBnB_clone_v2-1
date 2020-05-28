#!/usr/bin/python3
"""Instance of Flask"""


from flask import Flask, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models.base_model import BaseModel
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_places_all(place_id):
    """Gets all review of all places of a city."""
    data = storage.get('Place', place_id)
    if data is None:
        abort(404)
    new_dict = []
    for data in data.reviews:
        new_dict.append(data.to_dict())
    return jsonify(new_dict)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_places_by_id(review_id):
    """Gets a reviews of place all base form the id."""
    data_id = storage.get('Review', review_id)
    if data_id is None:
        abort(404)
    else:
        return jsonify(data_id.to_dict())


@app_views.route('/reviews/<review_id>', methods=['Delete'],
                 strict_slashes=False)
def delete_review_places_by_id(review_id):
    """Deletes a review of a places all base form the id."""
    data_id = storage.get('Review', review_id)
    if data_id is None:
        abort(404)
    storage.delete(data_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_a_review(place_id):
    """ Create a new review of a places."""
    if not storage.get("Place", place_id):
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if "user_id" not in data:
        abort(400, 'Missing user_id')
    if storage.get("User", data["user_id"]) is None:
        abort(404)
    if "text" not in data:
        abort(400, 'Missing text')
    new = Review(user_id=data["user_id"], text=data["text"], place_id=place_id)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_a_review_place(review_id):
    """ Update a old reviewed place."""
    first_review = storage.get('Review', review_id)
    if first_review is None:
        abort(404)
    is_json = request.get_json()
    if is_json is None:
        abort(400, "Not a JSON")
    dont = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in is_json.items():
        if key in dont:
            pass
        else:
            setattr(first_review, key, value)
    storage.save()
    return jsonify(first_review.to_dict()), 200
