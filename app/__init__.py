from app.config import Config
from flask import Flask

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	from app.views import views
	app.register_blueprint(views, url_prefix='/')

	return app