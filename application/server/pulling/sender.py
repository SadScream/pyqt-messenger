import datetime, time
from flask import Blueprint
from flask_login import login_required, current_user

from tools.response import * # noqa
from models.db_context import db, User, Message, UsernameHistory, ConnectionHistory # noqa

sender = Blueprint('sender', __name__)


@sender.route("/events/", methods=['GET'])
@login_required
def get_events():
	data = {
		"ok": True
	}

	delta = 60 * 60 * 24

	current_time = datetime.datetime.utcnow()
	day_ago = current_time - datetime.timedelta(seconds=60 * 60 * 24)

	_messages_history = db.session.query(Message).filter(Message.date >= day_ago).all()
	_nicknames_history = db.session.query(UsernameHistory).filter(UsernameHistory.date >= day_ago).all()
	_connection_history = db.session.query(ConnectionHistory).filter(ConnectionHistory.date >= day_ago).all()

	messages_history = []
	nicknames_history = []
	connection_history = []

	for obj in _messages_history:
		user = db.session.query(User).filter(User.user_id == obj.owner_id).first()

		msg = {
			"message_id": obj.message_id,
			"owner_id": obj.owner_id,
			"username": user.username,
			"text": obj.text,
			"date": obj.date.timestamp()
		}
		messages_history.append(msg)

	for obj in _nicknames_history:
		msg = {
			"user_id": obj.user_id,
			"old_username": obj.old_username,
			"new_username": obj.new_username,
			"date": obj.date.timestamp()
		}
		nicknames_history.append(msg)

	for obj in _connection_history:
		user = db.session.query(User).filter(User.user_id == obj.user_id).first()

		msg = {
			"user_id": obj.user_id,
			"is_connected": obj.is_connected,
			"username": user.username,
			"date": obj.date.timestamp()
		}
		connection_history.append(msg)

	data["messages"] = messages_history
	data["usernames"] = nicknames_history
	data["connections"] = connection_history

	return json_response(data) # noqa
