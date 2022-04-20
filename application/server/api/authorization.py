import datetime, time
from flask import Blueprint, request
from flask_login import login_required, current_user, logout_user, login_user

from tools.response import *  # noqa
from models.db_context import db, User, Message, MessageTypes  # noqa

auth_api = Blueprint('auth_api', __name__)


@auth_api.route('/sign-up/', methods=['POST'])
def sign_up():
	"""
	-> JSON {
		"username": str,
		"password": str
	}
	:return: JSON {'ok': true}
	"""

	data = {
		"ok": False
	}

	if current_user.is_authenticated:
		data["message"] = "Logged in"
		return json_response(data, 403)

	r = request.json
	username = r['username']
	password = r['password']

	user_obj = db.session.query(User).filter(User.username == username).first()

	if user_obj:
		data["message"] = "This username is already taken"
		return json_response(data, 406)

	if len(username) and len(password):
		user = User(username=username)
		user.set_password(password)

		db.session.add(user)
		db.session.commit()

		data["ok"] = True

		return json_response(data)

	return json_response(data, 401)


@auth_api.route('/login/', methods=['GET'])
def login():
	'''
	BasicAuth метод авторизации

	-> HEADERS:
		Authorization: Basic <username:password>  *BASE64*
	:return: {
		"ok": bool,
		"user_id": int,
		"message": str
	}
	'''

	data = {
		"ok": False
	}

	if current_user.is_authenticated:
		data["ok"] = True
		data["message"] = "You're already logged in"
		return json_response(data, 200)

	remember = True if request.args.get("remember") == "1" else False

	if request.authorization:
		username = request.authorization.username
		password = request.authorization.password
		user_obj = db.session.query(User).filter(User.username == username).first()

		if user_obj and user_obj.check_password(password):
			login_user(user_obj, remember=remember)
			data["ok"] = True
			data["user_id"] = user_obj.user_id

			event = Message(user_id=user_obj.user_id,
							msg_type=MessageTypes.CONNECTION,
							date=datetime.datetime.fromtimestamp(time.time()))
			db.session.add(event)
			db.session.commit()

			return json_response(data)

		data["message"] = "Invalid username/password"
		return json_response(data, 403)

	data["message"] = "BasicAuth needs"
	return json_response(data, 401)


@auth_api.route('/logout/')
@login_required
def logout():
	'''
	Выход из учетной записи

	:return: {
		"ok": bool
	}
	'''

	event = Message(user_id=current_user.user_id,
					msg_type=MessageTypes.DISCONNECTION,
					date=datetime.datetime.fromtimestamp(time.time()))
	logout_user()
	db.session.add(event)
	db.session.commit()
	return json_response({"ok": True})