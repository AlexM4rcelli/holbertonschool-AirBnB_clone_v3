#!/usr/bin/python3
"""_summary_

    Returns:
        _type_: _description_
    """
from . import app_views
from models import storage
from models.user import User
from flask import request, jsonify, abort


@app_views.route('/users',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def users_view():
    """_summary_

    Returns:
        _type_: _description_
    """
    if request.method == 'GET':
        amenities = storage.all(User).values()
        return jsonify([a.to_dict() for a in amenities])

    if request.method == 'POST':
        data = request.get_json()

        if data:
            if 'email' not in data:
                return jsonify({"error": "Missing email"}), 400
            elif 'password' not in data:
                return jsonify({"error": "Missing password"}), 400
            new = User(**data)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201

        return jsonify({"error": "Not a JSON"}), 400


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_by_id(user_id):
    """_summary_

    Args:
        user_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    user = storage.get(User, str(user_id))

    if user is None:
        return abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()

        if data:
            keys_to_ignore = ['id', 'email', 'created_at', 'updated_at']
            for key, val in data.items():
                if key not in keys_to_ignore:
                    setattr(user, key, val)
            storage.save()
            return jsonify(user.to_dict()), 200

        return jsonify({"error": "Not a JSON"}), 400
