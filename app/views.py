from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify
from app.models import User, Todo
from uuid import uuid4 as uv4
from app import db

views = Blueprint('views', __name__)

def get_objs(item):
	data = {}
	data['public_id'] = item.public_id
	data['name'] = item.name
	data['password'] = item.password
	data['admin'] = item.admin

	return data

@views.route('/')
def index():
	return {'data': 'Welcome to the flask api'}

@views.route('/user')
def get_users():
	users = User.query.all()

	output = []

	for usr in users:
		data = get_objs(usr)
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

@views.route('/user/<public_id>')
def get_user(public_id):
	user = User.query.filter(User.public_id == public_id).first()

	if not user:
		return jsonify({'message': 'No user found...'})
	
	data = get_objs(user)
	
	return jsonify({'user': data})

@views.route('/user/<user_id>', methods=['PUT'])
def updae_user(user_id):
	return ''

@views.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
	return ''

