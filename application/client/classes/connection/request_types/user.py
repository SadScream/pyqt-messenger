from .default_connection import DefaultConnection

try:
	from errors import UsernameAlreadyTaken
	from decorators import auth_required
except ModuleNotFoundError:
	from ..errors import UsernameAlreadyTaken
	from ..decorators import auth_required


class User(DefaultConnection):

	def __init__(self, host=None):
		super().__init__(host)

		self.api_users = self._api + "users/"  # GET or POST
		self.api_user = self._api + 'users/%s'  # should contain user id or nickname

	@auth_required
	def change_nickname(self, new_username: str):
		r = self.session.post(url=self.api_users, json={
			"new_username": new_username,
		})

		result = r.json()

		if not result["ok"] and r.status_code == 409:
			raise UsernameAlreadyTaken()

		return r

	@auth_required
	def get_users(self):
		r = self.session.get(self.api_users)
		return r

	@auth_required
	def get_user(self, user_id: int):
		r = self.session.get(self.api_user % user_id)
		return r

	@auth_required
	def get_user(self, username: str):
		r = self.session.get(self.api_user % username)
		return r