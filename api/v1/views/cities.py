#!/usr/bin/python3
"""
States view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities',
                 strict_slashes=False,
                 methods=["GET"])
def get_all_city(state_id):
    """Retrieves the list of all State objects"""
    cities = storage.all(City)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_objs = []
    for obj in cities.values():
        if obj.state_id == state_id:
            city_objs.append(obj.to_dict())
    return jsonify(city_objs)


@app_views.route('/cities/<string:city_id>',
                 strict_slashes=False,
                 methods=["GET"])
def get_city(city_id):
    """Retrieves a State object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<string:city_id>',
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_city(city_id):
    """Delete a State object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<string:state_id>/cities',
                 strict_slashes=False,
                 methods=["POST"])
def create_city(state_id):
    """Creates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, "Not a JSON")
    if 'name' in req:
        city = City(**req, state_id=state_id)
        city.save()
        return jsonify(city.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route('/cities/<string:city_id>',
                 strict_slashes=False,
                 methods=["PUT"])
def update_city(city_id):
    """Update a State object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, "Not a JSON")
    else:
        for key, value in req.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
