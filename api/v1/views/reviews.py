#!/usr/bin/env python

from . import app_views
from models import storage
from models.place import Place
from models.review import Review
from flask import request, jsonify, abort

@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def reviews_view(place_id):
    place = storage.get(Place, str(place_id))
    if place is None:
        return abort(404)

    if request.method == 'GET':
        return jsonify([review.to_dict() for review in place.places])
    
    if request.method == 'POST':
        data = request.get_json()

        if data:
            if 'user_id' not in data:
                return jsonify({"error": "Missing user_id"}), 400
            elif 'text' not in data:
                return jsonify({"error": "Missing text"}), 400

            from models.user import User
            if storage.get(User, str(data['user_id'])) is None:
                return abort(404)

            new = Review(**data)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201

        return jsonify({"error": "Not a JSON"}), 400


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review_by_id(review_id):
    review = storage.get(Review, str(review_id))
    
    if review is None:
        return abort(404)
    
    if request.method == 'GET':
        return jsonify(review.to_dict())
    
    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return jsonify({}), 200
    
    if request.method == 'PUT':
        data = request.get_json()

        if data:
            keys_to_ignore = [
                              'id', 'user_id', 'place_id',
                              'created_at', 'updated_at'
                              ]
            for key, val in data.items():
                if key not in keys_to_ignore:
                    setattr(review, key, val)
            storage.save()
            return jsonify(review.to_dict()), 200
            
        return jsonify({"error": "Not a JSON"}), 400