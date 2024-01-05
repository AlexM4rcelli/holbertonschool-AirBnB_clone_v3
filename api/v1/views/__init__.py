#!/usr/bin/python3
from flask import Blueprint
from . import index, states, cities, amenities, users, places, reviews
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
