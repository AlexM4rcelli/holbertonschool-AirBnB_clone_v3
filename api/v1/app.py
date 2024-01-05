#!/usr/bin/python3
"""_summary_

    Returns:
        _type_: _description_
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import storage
from .views import app_views


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(exception=None):
    """Handles 404 errors by returning a JSON response"""
    return jsonify({"error": "Not found"})


@app.teardown_appcontext
def teardown(exception=None):
    """closes the storage"""
    return storage.close()


if __name__ == '__main__':
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'),
            threaded=True)
