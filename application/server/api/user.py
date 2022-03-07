import datetime, time
from flask import Blueprint, request
from flask_login import login_required, current_user, logout_user

from tools.response import *
from models.db_context import db, User, Message, MessageTypes

user_api = Blueprint('user_api', __name__)


@user_api.route("/users/", methods=['GET'])
@login_required
def get_users():
	users = []
	data = {
		"ok": False
	}

	_users = db.session.query(User).all()

	for u in _users:
		user = {
			"user_id": u.user_id,
			"username": u.username,
		}
		users.append(user)

	data["ok"] = True
	data["users"] = users
	return data


@user_api.route("/users/", methods=['POST'])
@login_required
def change_username():
	"""
	-> JSON {
		"new_username": str
	}
	:return: JSON {'ok': true}
	"""

	r = request.json
	username = r["new_username"]

	data = {
		"ok": False
	}

	user_obj = db.session.query(User).filter(User.username == username).first()

	if user_obj:
		data["message"] = "Username already taken"
		return json_response(data, 409) # noqa
	elif len(username):
		old_username = current_user.username
		current_user.username = username

		db.session.add(current_user)
		db.session.commit()

		data["ok"] = True

		event = Message(user_id=current_user.user_id,
						msg_type=MessageTypes.NAME_CHANGED,
						old_username=old_username,
						new_username=current_user.username,
						date=datetime.datetime.fromtimestamp(time.time()))
		db.session.add(event)
		db.session.commit()

		return json_response(data)  # noqa

	return json_response(data)  # noqa


@user_api.route("/users/<int:user_id>", methods=['GET'])
@login_required
def get_user_by_id(user_id):
	user_obj = db.session.query(User).filter(User.user_id == user_id).first()

	data = {
		"ok": False
	}

	if user_obj:
		data["ok"] = True
		data["user_id"] = user_obj.user_id
		data["username"] = user_obj.username

		return json_response(data)

	return json_response(data, 404)


@user_api.route("/users/<string:username>", methods=['GET'])
@login_required
def get_user_by_username(username):
	user_obj = db.session.query(User).filter(User.username == username).first()

	data = {
		"ok": False
	}

	if user_obj:
		data["ok"] = True
		data["user_id"] = user_obj.user_id
		data["username"] = user_obj.username

		return json_response(data)

	return json_response(data, 404)