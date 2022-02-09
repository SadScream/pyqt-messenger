import datetime
from flask import Blueprint, request
from flask_login import login_required, current_user, logout_user

from tools.response import *
from models.db_context import db, User, Message

msg_api = Blueprint('msg_api', __name__)


@msg_api.route("/messages/", methods=['POST'])
@login_required
def send_message():
	"""
	-> JSON {
		"text": str,
		"date": float
	}
	:return: JSON {'ok': true}
	"""

	r = request.json
	text = r["text"]
	date = datetime.datetime.fromtimestamp(r["date"])

	data = {
		"ok": False
	}

	if current_user:
		message_obj = Message(owner_id=current_user.user_id, text=text, date=date)
		db.session.add(message_obj)
		db.session.commit()

		data["ok"] = True
		return json_response(data)

	data["message"] = "User not found"
	return json_response(data, 404)


@msg_api.route("/messages/", methods=['GET'])
@login_required
def get_messages():
	messages = []
	data = {
		"ok": False
	}

	_messages = db.session.query(Message).all()

	for m in _messages:
		msg = {
			"message_id": m.message_id,
			"owner_id": m.owner_id,
			"text": m.text,
			"date": m.date.timestamp()
		}
		messages.append(msg)

	data["ok"] = True
	data["messages"] = messages
	return json_response(data, 404)


@msg_api.route("/messages/<int:message_id>", methods=['GET'])
@login_required
def get_message(message_id):
	message_obj = db.session.query(User).filter(Message.message_id == message_id).first()

	data = {
		"ok": False
	}

	if message_obj:
		data["ok"] = True
		data["message_id"] = message_obj.message_id
		data["owner_id"] = message_obj.owner_id
		data["text"] = message_obj.text
		data["date"] = message_obj.date.timestamp()

		return json_response(data)

	return json_response(data, 404)