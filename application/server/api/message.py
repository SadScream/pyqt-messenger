import datetime
from flask import Blueprint, request
from flask_login import login_required, current_user, logout_user

from tools.response import *
from models.db_context import db, User, Message, MessageTypes

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
		message_obj = Message(user_id=current_user.user_id, text=text, msg_type=MessageTypes.NEW_MESSAGE, date=date)
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

	current_time = datetime.datetime.utcnow()
	day_ago = current_time - datetime.timedelta(seconds=60 * 60 * 24)

	_messages = db.session.query(Message).filter(Message.date >= day_ago).all()

	for m in _messages:
		msg = {
			"message_id": m.message_id,
			"user_id": m.user_id,
			"type": m.msg_type,
			"text": m.text,
			"date": m.date.timestamp()
		}

		if m.msg_type in (MessageTypes.NEW_MESSAGE, MessageTypes.CONNECTION, MessageTypes.DISCONNECTION):
			user = db.session.query(User).filter(User.user_id == m.user_id).first()
			msg["username"] = user.username
		elif m.msg_type == MessageTypes.NAME_CHANGED:
			msg["old_username"] = m.old_username
			msg["new_username"] = m.new_username

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
		data["user_id"] = message_obj.user_id
		data["type"] = message_obj.msg_type
		data["text"] = message_obj.text
		data["date"] = message_obj.date.timestamp()

		if message_obj.msg_type in (MessageTypes.NEW_MESSAGE, MessageTypes.CONNECTION, MessageTypes.DISCONNECTION):
			user = db.session.query(User).filter(User.user_id == message_obj.user_id).first()
			data["username"] = user.username
		elif message_obj.msg_type == MessageTypes.NAME_CHANGED:
			data["old_username"] = message_obj.old_username
			data["new_username"] = message_obj.new_username

		return json_response(data)

	return json_response(data, 404)