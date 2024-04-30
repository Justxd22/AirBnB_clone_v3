#!/usr/bin/python3
"""
Init.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city(city_id):
    """Cities endpoint."""
    c = storage.get('City', city_id)
    if not c:
        abort(404)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        dkey = ['id', 'created_at', 'updated_at']
        for key, val in request.json.items():
            if key not in dkey:
                setattr(c, key, val)
        c.save()
        return jsonify(c.to_dict()), 200

    if request.method == 'GET':
        return jsonify(c.to_dict())

    if request.method == 'DELETE':
        storage.delete(c)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities_of_State(state_id):
    """Cities endpoint."""
    state = storage.get('State', state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        nc = City(**request.get_json())
        nc.state_id = state.id
        nc.save()
        return jsonify(nc.to_dict()), 201
