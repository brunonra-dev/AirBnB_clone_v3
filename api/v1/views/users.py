#!/usr/bin/python3
"""
User view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=["GET"])
def get_all_users():
    """Retrieves the list of all users objects"""
    objs = storage.all(User)
    all_objs = []
    for obj in objs.values():
        all_objs.append(obj.to_dict())
    return jsonify(all_objs)


@app_views.route('/users/<string:user_id>',
                 strict_slashes=False,
                 methods=["GET"])
def get_user(user_id):
    """Retrieves a User object"""
    obj = storage.get(User, user_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/users/<string:user_id>',
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_user(user_id):
    """Delete a User object"""
    obj = storage.get(User, user_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=["POST"])
def create_user():
    """Creates an User object"""
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, "Not a JSON")
    if 'email' not in req:
        abort(400, "Missing email")
    if 'password' not in req:
        abort(400, "Missing password")
    am = User(**req)
    am.save()
    return jsonify(am.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 strict_slashes=False,
                 methods=["PUT"])
def update_user(user_id):
    """Update a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    req = request.get_json(force=True, silent=True)
    if req is None:
        abort(400, "Not a JSON")
    else:
        for key, value in req.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
