#!/usr/bin/python3
"""_summary_

    Returns:
        _type_: _description_
"""
from . import app_views
from models import storage
from flask import jsonify, request

@app_views.route('/status', strict_slashes=False)
def status():
    """_summary_

    Returns:
        _type_: _description_
    """
    if request.method == 'GET':
        return jsonify({
        "status": "OK"
    })

@app_views.route('/stats', strict_slashes=False)
def stats():
    """_summary_

    Returns:
        _type_: _description_
    """
    if request.method == 'GET':
        response_data = {
            "amenities": storage.count('Amenity'),
            "cities": storage.count('City'),
            "places": storage.count('Place'),
            "reviews": storage.count('Review'),
            "states": storage.count('State'),
            "users": storage.count('User')
        }
        return jsonify(response_data)
