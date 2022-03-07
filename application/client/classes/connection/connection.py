try:
	from errors import *
	from request_types.authorization import Authorization
	from request_types.message import Message
	from request_types.user import User
	from request_types.events import Events
except ModuleNotFoundError:
	from .errors import *
	from .request_types.authorization import Authorization
	from .request_types.message import Message
	from .request_types.user import User
	from .request_types.events import Events

from requests import exceptions


class Connection(Authorization, Message, User, Events):

	def __init__(self, host=None):
		super().__init__(host)

	def ping(self, host=None):
		if host is None:
			host = self.host

		try:
			r = self.session.get(host)
		except Exception:
			raise ServerUnavailableError("Given host doesn't respond")

		if ("ok" not in r.json()) or (not r.json()["ok"]):
			raise ServerUnavailableError("Given host doesn't respond")

	def set_host(self, host: str):
		self.ping(host)
		self.host = host


if __name__ == '__main__':
	connection = Connection()
	# connection.registration("saddy", "123")
	connection.login("saddy", "123")
	# connection.send_message("hello", time.time())
	# response = connection.get_messages()
	# print(response)
	# response = connection.get_users()
	# print(response)
	# response = connection.get_user(1)
	# print(response)
	# connection.change_nickname("sadscream")
	# response = connection.get_user(1)
	# print(response)
	response = connection.get_events()
	print(response)
