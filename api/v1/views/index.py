#!/usr/bin/python3
"""
Init.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classe


@app_views.route("/status", strict_slashes=False)
def status():
    """Status endpoint."""
    return jsonify(status="OK")


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Stats endpoint."""
    c = classe
    for x in c:
        c[x] = storage.count(c[x])
    return jsonify(c)
