#!/usr/bin/python3
"""Instance of Flask"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


app = Flask(__name__)


@app_views.route("/status")
def json_status():
    """ Returns Dummy Text."""
    return jsonify(status='OK')


@app_views.route("/stats")
def count_classes():
    """
        method to return a jsonified dictionary of stats.
    """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
