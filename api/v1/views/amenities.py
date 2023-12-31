#!/usr/bin/env python

from . import app_views
from models import storage
from models.amenity import Amenity
from flask import request, jsonify, abort

@app_views.route('/amenities',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def amenities_view():
    if request.method == 'GET':
        amenities = storage.all(Amenity).values()
        return jsonify([a.to_dict() for a in amenities])
    
    if request.method == 'POST':
        data = request.get_json()

        if data:
            if 'name' not in data:
                return jsonify({"error": "Missing name"}), 400
            new = Amenity(**data)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201

        return jsonify({"error": "Not a JSON"}), 400


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    amenity = storage.get(Amenity, str(amenity_id))
    
    if amenity is None:
        return abort(404)
    
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    
    if request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    
    if request.method == 'PUT':
        data = request.get_json()

        if data:
            keys_to_ignore = ['id', 'created_at', 'updated_at']
            for key, val in data.items():
                if key not in keys_to_ignore:
                    setattr(amenity, key, val)
            storage.save()
            return jsonify(amenity.to_dict()), 200
            
        return jsonify({"error": "Not a JSON"}), 400