from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify
from app.models import User, Todo
from uuid import uuid4 as uv4
from app import db

views = Blueprint('views', __name__)

@views.route('/')
def index():
	return {'data': 'Welcome to the flask api'}

@views.route('/user')
def get_users():
	users = User.query.all()

	output = []

	for usr in users:
		data = {}
		data['public_id'] = usr.public_id
		data['name'] = usr.name
		data['password'] = usr.password
		data['admin'] = usr.admin
		output.append(data)

	return jsonify({'users': output})

@views.route('/user', methods=['POST'])
def create_user():
	data = request.get_json()
	hashed_pwd = generate_password_hash(data['password'], method='sha256')

	new_user = User(public_id=str(uv4()), name=data['name'], password=hashed_pwd, admin=False)
	db.session.add(new_user)
	db.session.commit()

	return jsonify({'message': 'New user created'})

@views.route('/user/<user_id>')
def get_user(user_id):
	return ''

@views.route('/user/<user_id>', methods=['PUT'])
def updae_user(user_id):
	return ''

@views.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
	return ''

