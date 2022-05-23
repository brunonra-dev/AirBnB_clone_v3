#!/usr/bin/python3
"""
Places view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places',
                 strict_slashes=False,
                 methods=["GET"])
def get_all_places(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all(Place)
    list_places = []
    for obj in places.values():
        if obj.city_id == city_id:
            list_places.append(obj.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<string:place_id>',
                 strict_slashes=False,
                 methods=["GET"])
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<string:place_id>',
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_place(place_id):
    """Delete a Place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<string:city_id>/places',
                 strict_slashes=False,
                 methods=["POST"])
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place = request.get_json(force=True, silent=True)
    user = storage.get(User, place['user_id'])
    if place is None:
        abort(400, "Not a JSON")
    if 'name' not in place:
        abort(400, "Missing name")
    if 'user_id' not in place.keys():
        abort(400, "Missing user_id")
    if user is None:
        abort(404)
    new = Place(**place, city_id=city_id)
    storage.new(new)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 strict_slashes=False,
                 methods=["PUT"])
def update_place(place_id):
    """Update a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, "Not a JSON")
    else:
        for key, value in req.items():
            if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
