from flask import Flask, request, abort
import datetime
import time

from json_handler import Json_handler


app = Flask(__name__)
config = Json_handler()


def event(type_:str, user_id:int, **kwargs):
	current_time = time.time()
	e = {"type": type_, "user_id": user_id, "time": current_time}
	e.update(kwargs)

	return e


@app.route("/", methods=['POST'])
def main_page():
	"""
	-> JSON {
		"key": int,
	}
	:return: JSON {
		"ok": bool
	}
	"""

	key = request.json["key"]

	if key == "_scream_":
		return {"ok": True}
	else:
		return {"ok": False}


@app.route("/user.getUsernames", methods=['GET'])
def get_nicknames():
	"""
	:return: JSON {
		"usernames": list
	}
	"""

	usernames = []

	for user in config.read_field("users"):
		usernames.append(list(user.values())[0])

	return {"usernames": usernames}


@app.route("/user.check", methods=['POST'])
def check_id():
	"""
	-> JSON {
		"user_id": int,
	}
	:return: JSON {
		"ok": bool
		"user_id": int
	}
	"""

	user_id = request.json["user_id"]

	if user_id >= 0 and user_id <= config.most_user_id:
		return {"ok": True, "user_id": user_id}
	else:
		return {"ok": False, "user_id": user_id}


@app.route("/user.getid", methods=['POST'])
def get_id():
	"""
	-> JSON {
		"nickname": str,
	}
	:return: JSON {
		"user_id": int
	}
	"""

	n = config.most_user_id
	nickname = request.json["nickname"]

	config.write_user(n, nickname)

	return {"user_id": n}


@app.route("/messages.send", methods=['POST'])
def send_message():
	"""
	-> JSON {
		"user_id": int,
		"message": str
	}
	:return: JSON {'ok': true}
	"""

	r = request.json
	user_id = r["user_id"]
	message = r["message"]

	config.write_event(event(type_="messages.send", user_id=user_id, message=message, username=config.read_username(user_id)))

	return {"ok": True}


@app.route("/user.connect", methods=['POST'])
def connect():
	"""
	-> JSON {
		"user_id": int
	}
	:return: {'ok': true}
	"""

	user_id = request.json["user_id"]
	config.write_event(event(type_="user.connect", user_id=user_id, username=config.read_username(user_id)))

	return {'ok': True}


@app.route("/user.disconnect", methods=['POST'])
def disconnect():
	"""
	-> JSON {
		"user_id": int
	}
	:return: {'ok': true}
	"""

	user_id = request.json["user_id"]
	config.write_event(event(type_="user.disconnect", user_id=user_id, username=config.read_username(user_id)))

	return {'ok': True}


@app.route("/user.rename", methods=['POST'])
def nick_change():
	"""
	-> JSON {
		"id": int,
		"nickname": str
	}
	:return: JSON {
		"ok": true
	}
	"""

	user_id = request.json["id"]
	nickname = request.json["nickname"]

	for user in config.read_field("users"):
		if list(user.values())[0] == nickname:
			return {"ok": False}

	config.change_user_nickname(user_id, nickname)

	config.write_event(
		event(
			type_="user.rename", user_id=user_id,
			confirmed=True,
			old_name=config.read_username(user_id), 
			new_name=nickname))

	return {"ok": True}


@app.route("/events.get", methods=['POST'])
def get_events():
	"""
	-> JSON {
		"after": float
	}
	:return: JSON {
		"events": [
			{ "type": str, "user_id": str, "message": str, "time": float }
			...
		]
	}
	"""

	after = request.json["after"]
	filtered_events = [
		event for event in config.read_field("events") if event['time'] > after
		]

	return {
		'events': filtered_events
	}


@app.route("/events.getAll", methods=['POST'])
def get_all_events():
	"""
	-> JSON {
		"after": float
	}
	:return: JSON {
		"events": [
			{ "type": str, "user_id": str, "message": str, "time": float }
			...
		]
	}
	"""

	return {
		'events': config.read_field("events")
	}


if __name__ == "__main__":
	app.run()
	config.close()
