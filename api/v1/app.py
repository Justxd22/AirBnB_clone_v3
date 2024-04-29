from flask import Flask, request, jsonify, render_template, send_from_directory
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def dn(e):
    storage.close()


@app.route("/hello", methods=['GET'])
def web():
    return "HELLO"


if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST", "0.0.0.0"),
            port=os.getenv("HBNB_API_PORT", "5000"),
            threaded=True)
