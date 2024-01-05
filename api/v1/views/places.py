#!/usr/bin/python3
"""_summary_

    Returns:
        _type_: _description_
    """
from . import app_views
from models import storage
from models.place import Place
from models.city import City
from flask import request, jsonify, abort


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def places_view(city_id):
    """_summary_

    Args:
        city_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    city = storage.get(City, str(city_id))
    if city is None:
        return abort(404)

    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])

    if request.method == 'POST':
        data = request.get_json()

        if data:
            if 'name' not in data:
                return jsonify({"error": "Missing name"}), 400
            elif 'user_id' not in data:
                return jsonify({"error": "Missing user_id"}), 400

            from models.user import User
            if storage.get(User, str(data['user_id'])) is None:
                return abort(404)

            new = Place(**data)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201

        return jsonify({"error": "Not a JSON"}), 400


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_by_id(place_id):
    """_summary_

    Args:
        place_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    place = storage.get(Place, str(place_id))

    if place is None:
        return abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()

        if data:
            keys_to_ignore = [
                              'id', 'user_id', 'city_id',
                              'created_at', 'updated_at'
                              ]
            for key, val in data.items():
                if key not in keys_to_ignore:
                    setattr(place, key, val)
            storage.save()
            return jsonify(place.to_dict()), 200

        return jsonify({"error": "Not a JSON"}), 400
