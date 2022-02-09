from .default_connection import DefaultConnection

try:
	from decorators import auth_required
except ModuleNotFoundError:
	from ..decorators import auth_required


class Message(DefaultConnection):

	def __init__(self, host=None):
		super().__init__(host)

		self.api_messages = self._api + "messages/"  # GET or POST
		self.api_get_message = self._api + 'message/%s'  # should contain message id

	@auth_required
	def send_message(self, message: str, date: float):
		r = self.session.post(url=self.api_messages, json={
			"text": message,
			"date": date
		})

		return r

	@auth_required
	def get_messages(self):
		r = self.session.get(self.api_messages)
		return r