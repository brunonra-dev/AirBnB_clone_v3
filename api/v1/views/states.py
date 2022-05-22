#!/usr/bin/python3
"""
States view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=["GET"])
def get():
    """Retrieves the list of all State objects"""
    objs = storage.all(State)
    all_objs = []
    for obj in objs.values():
        all_objs.append(obj.to_dict())
    return jsonify(all_objs)


@app_views.route('/states/<string:state_id>',
                 strict_slashes=False,
                 methods=["GET"])
def get_state(state_id):
    """Retrieves a State object"""
    obj = storage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/states/<string:state_id>',
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id):
    """Delete a State object"""
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=["POST"])
def create_state():
    """Creates a State object"""
    req = request.get_json(force=True)
    if "application/json" in request.headers["Content-Type"]:
        if 'name' in req:
            st = State(**req)
            st.save()
            return jsonify(st.to_dict()), 201
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route('/states/<string:state_id>',
                 strict_slashes=False,
                 methods=["PUT"])
def update_state(state_id):
    """Update a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req = request.get_json(force=True)
    if req is None:
        abort(400, "Not a JSON")
    else:
        for key, value in req.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
