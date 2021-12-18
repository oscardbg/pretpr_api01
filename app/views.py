from os import altsep
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, json, request, jsonify, make_response
from datetime import datetime, timedelta
from app.models import User, Todo
from app.config import Config
from uuid import uuid4 as uv4
from functools import wraps
from app import db
import jwt

views = Blueprint('views', __name__)

def get_objs(item):
	data = {}
	data['public_id'] = item.public_id
	data['name'] = item.name
	data['password'] = item.password
	data['admin'] = item.admin

	return data

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['SH256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@views.route('/')
def index():
	return {'data': 'Welcome to the flask api'}

@views.route('/user')
@token_required
def get_users(current_user):
	if not current_user.admin:
		return jsonify({'message': 'Cannot perform that function...'})

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
		resp = {'message': 'No user found...'}
	else:
		data = get_objs(user)
		resp = {'user': data}
	
	return jsonify(resp)

@views.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id):
	user = User.query.filter(User.public_id == public_id).first()

	if not user:
		resp = {'message': 'No user found...'}
	else:
		user.admin = True
		db.session.commit()
		resp = {'message': 'User promoted to admin...'}

	return jsonify(resp)

@views.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
	user = User.query.filter_by(public_id=public_id).first()

	if not user:
		resp = {'message': 'Not user found...'}
	else:
		db.session.delete(user)
		db.session.commit()
		resp = {'message': 'Selected user deleted'}
	
	return jsonify(resp)

@views.route('/login')
def login():
	auth = request.authorization

	if not auth or not auth.username or not auth.password:
		return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

	user = User.query.filter_by(name=auth.username).first()

	if not user:
		#return jsonify({'message': 'No user found...'})
		return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

	if check_password_hash(user.password, auth.password):
		token = jwt.encode({'public_id': user.public_id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, Config.SECRET_KEY, algorithm='HS256')
		#return jsonify({'token': jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256']) })
		return jsonify({'token': token})
	
	return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})