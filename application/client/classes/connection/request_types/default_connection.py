import requests


class DefaultConnection:
	host: str = "http://127.0.0.1:5000/"
	session: requests.Session
	_api = '%sapi/'

	def __init__(self, host=None):
		if host is not None:
			self.host = host

		self._api = self._api % self.host
		self.session = requests.Session()