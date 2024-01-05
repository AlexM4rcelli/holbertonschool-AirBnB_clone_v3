#!/usr/bin/python3
"""_summary_

    Returns:
        _type_: _description_
    """
from . import app_views
from models import storage
from models.city import City
from models.state import State
from flask import request, jsonify, abort


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def cities_view(state_id):
    """_summary_

    Args:
        state_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    state = storage.get(State, str(state_id))

    if state is None:
        return abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])

    if request.method == 'POST':
        data = request.get_json()

        if data:
            if 'name' not in data:
                return jsonify({"error": "Missing name"}), 400
            new = City(**data)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201

        return jsonify({"error": "Not a JSON"}), 400


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_by_id(city_id):
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
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()

        if data:
            keys_to_ignore = ['id', 'created_at', 'updated_at']
            for key, val in data.items():
                if key not in keys_to_ignore:
                    setattr(city, key, val)
            storage.save()
            return jsonify(city.to_dict()), 200

        return jsonify({"error": "Not a JSON"}), 400
