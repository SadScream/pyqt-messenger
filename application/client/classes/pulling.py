import time
import threading
from requests.exceptions import ConnectionError

from .connection.connection import Connection


class Puller:
	serve = False
	connection: Connection
	thread: threading.Thread
	last_datetime: float = 0
	event_listener = None  # функция, которая будет вызываться при появлении новых событий
	error_catched = False

	def __init__(self, connection, event_listener):
		self.connection = connection
		self.event_listener = event_listener

	def start_pulling(self):
		self.serve = True
		self.error_catched = False
		self.thread = threading.Thread(target=self.pull_forever)
		self.thread.start()

	def stop_pulling(self):
		self.serve = False
		self.last_datetime = 0

	def pull_forever(self):
		while self.serve:
			self.pull_once()
			time.sleep(0.3)

	def pull_once(self):
		try:
			response: list = self.connection.get_messages()

			if self.error_catched:
				self.error_catched = False
		except ConnectionError as E:
			if self.error_catched:
				return

			self.error_catched = True
			self.event_listener(E)
			return

		response = sorted(response['messages'], key=lambda obj: obj["date"])

		if len(response) and response[-1]["date"] > self.last_datetime:
			if self.event_listener:
				self.event_listener(list(filter(lambda obj: obj["date"] > self.last_datetime, response)))

			self.last_datetime = response[-1]["date"]
