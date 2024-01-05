#!/usr/bin/python3
"""_summary_
"""
from . import app_views
from models import storage
from models.state import State
from flask import request, jsonify, abort


@app_views.route('/states',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def state_view():
    """_summary_

    Returns:
        _type_: _description_
    """
    if request.method == 'GET':
        states = storage.all(State).values()
        state_list = [state.to_dict() for state in states]

        return jsonify(state_list)

    if request.method == 'POST':
        data = request.get_json()

        if data:
            if 'name' not in data:
                return jsonify({"error": "Missing name"}), 400
            new = State(**data)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201

        return jsonify({"error": "Not a JSON"}), 400


@app_views.route('states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_by_id(state_id):
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
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()

        if data:
            keys_to_ignore = ['id', 'created_at', 'updated_at']
            for key, val in data.items():
                if key not in keys_to_ignore:
                    setattr(state, key, val)
            storage.save()
            return jsonify(state.to_dict()), 200

        return jsonify({"error": "Not a JSON"}), 400
