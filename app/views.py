from flask import Blueprint, request, jsonify

views = Blueprint('views', __name__)

@views.route('/')
def index():
	return {'data': 'Welcome to the flask api'}