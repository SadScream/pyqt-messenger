import time
import threading
from requests.exceptions import ConnectionError

from .connection.connection import Connection


class Puller:
	serve = False
	connection: Connection
	thread: threading.Thread
	last_event: dict = None
	event_listener = None
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

	def pull_forever(self):
		while self.serve:
			self.pull_once()
			time.sleep(0.3)

	def pull_once(self):
		try:
			response: list = self.connection.get_events()

			if self.error_catched:
				self.error_catched = False
		except ConnectionError as E:
			if self.error_catched:
				return

			self.error_catched = True
			self.event_listener(E)
			return

		response = sorted(response, key=lambda obj: obj["date"])

		if response and response[-1] != self.last_event:
			try:
				start = response.index(self.last_event)
			except ValueError:
				start = 0

			self.last_event = response[-1]

			if self.event_listener:
				self.event_listener(response[start+1:])