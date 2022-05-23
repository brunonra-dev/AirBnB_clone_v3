#!/usr/bin/python3
"""
starts a Flask web application
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(ex):
    """calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': "Not found"}), 404


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', default='0.0.0.0'),
            port=getenv('HBNB_API_PORT', default='5000'),
            threaded=True)
