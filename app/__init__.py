from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from os.path import exists
from flask import Flask

db = SQLAlchemy()
DB_NAME = 'apidata.db'

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)

	from app.views import views
	app.register_blueprint(views, url_prefix='/')

	create_db(app)

	return app

def create_db(app):
	if not exists('app/' + DB_NAME):
		db.create_all(app=app)
		print(' • DB created...!')