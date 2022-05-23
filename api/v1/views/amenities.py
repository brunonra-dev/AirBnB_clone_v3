#!/usr/bin/python3
"""
States view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=["GET"])
def get_all_amenities():
    """Retrieves the list of all Amenities objects"""
    objs = storage.all(Amenity)
    all_objs = []
    for obj in objs.values():
        all_objs.append(obj.to_dict())
    return jsonify(all_objs)


@app_views.route('/amenities/<string:amenity_id>',
                 strict_slashes=False,
                 methods=["GET"])
def get_amenity(amenity_id):
    """Retrieves a Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<string:amenity_id>',
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id):
    """Delete a Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=["POST"])
def create_amenity():
    """Creates an Amenity object"""
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, "Not a JSON")
    if 'name' in req:
        am = Amenity(**req)
        am.save()
        return jsonify(am.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route('/states/<string:amenity_id>',
                 strict_slashes=False,
                 methods=["PUT"])
def update_amenity(amenity_id):
    """Update a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, "Not a JSON")
    else:
        for key, value in req.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
