#!/usr/bin/env python3

from flask import Flask, jsonify, request, abort 

from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.before_request
def before_request():
    """ Example function """
    pass


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ Remove current SQLAlchemy session """
    storage.close()


@app.route('/status', methods=['GET'])
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app.route('/stats', methods=['GET'])
def stats():
    """Returns the number of each object type"""
    return jsonify(storage.count())
