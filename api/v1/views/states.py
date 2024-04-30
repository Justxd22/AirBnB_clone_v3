#!/usr/bin/python3
"""
Init.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states():
    """States endpoint."""
    a = storage.all('State')
    li = []
    for x in a.values():
        li.append(x.to_dict())
    return jsonify(li)


@app_views.route('/states/<state>', methods=['GET'],
                 strict_slashes=False)
def statebyid(state):
    """States endpoint."""
    o = storage.get('State', state)
    if o is None:
        abort(404)
    return jsonify(o.to_dict(), 200)


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def setstate():
    """States endpoint."""
    if not request.json:
        abort(400, {'Not a JSON'})
    if "name" not in request.get_json():
        abort(400, {'Missing name'})
    s = State(**request.get_json())
    storage.new(s)
    storage.save()
    return jsonify(s.to_dict()), '201'


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def upstate(state_id):
    """States endpoint."""
    if not request.json:
        abort(400, {'Not a JSON'})
    s = storage.get(State, state_id)
    if s is None:
        abort(404)
    dkey = ['id', 'created_at', 'updated_at']
    for key, val in request.json.items():
        if key not in dkey:
            setattr(s, key, val)
    s.save()
    return jsonify(s.to_dict()), '200'


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleting(state_id):
    """States endpoint."""
    s = storage.get(State, state_id)
    if s is None:
        abort(404)
    storage.delete(s)
    storage.save()
    return jsonify({}), '200'
