from .default_connection import DefaultConnection

try:
	from decorators import auth_required, merge_data
except ModuleNotFoundError:
	from ..decorators import auth_required, merge_data


class Events(DefaultConnection):

	def __init__(self, host=None):
		super().__init__(host)
		self.events = self.host + "events/"

	@merge_data
	@auth_required
	def get_events(self):
		r = self.session.get(url=self.events)
		return r