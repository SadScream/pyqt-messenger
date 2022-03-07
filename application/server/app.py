# -*- coding: utf-8 -*-

from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from sqlalchemy import exc

from config import *
from models.db_context import db, User
from tools.response import make_response
from api import user, message, authorization

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{USERNAME}:{PASSWORD}@{HOST}/{DB_NAME}'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

migrate = Migrate(app, db, compare_type=True)

app.register_blueprint(user.user_api, url_prefix="/api")
app.register_blueprint(message.msg_api, url_prefix="/api")
app.register_blueprint(authorization.auth_api, url_prefix="/api")


@login_manager.user_loader
def load_user(user_id):
	try:
		return db.session.query(User).get(user_id)
	except exc.OperationalError:
		return db.session.query(User).get(user_id)


@app.route("/", methods=['POST', 'GET'])
def main_page():
	return {"ok": True}


def unauthorized():
	return make_response({"ok": False}, 401)


login_manager.unauthorized_callback = unauthorized

if __name__ == "__main__":
	app.run()
