from requests.auth import HTTPBasicAuth

from .default_connection import DefaultConnection

try:
	from errors import (RegistrationWhileLoggedIn, UsernameAlreadyTaken,
						InvalidLoginOrPassword, AlreadyLoggedIn)
	from decorators import auth_required
except ModuleNotFoundError:
	from ..errors import (RegistrationWhileLoggedIn, UsernameAlreadyTaken,
						InvalidLoginOrPassword, AlreadyLoggedIn)
	from ..decorators import auth_required


class Authorization(DefaultConnection):
	def __init__(self, host=None):
		super().__init__(host)

		self.logged_in = False
		self.api_signup = self._api + "sign-up/"
		self.api_login = self._api + "login/"
		self.api_logout = self._api + "logout/"

	def registration(self, username, password):
		r = self.session.post(url=self.api_signup, json={
			"username": username,
			"password": password
		})

		result = r.json()

		if not result["ok"]:
			if r.status_code == 403:
				raise RegistrationWhileLoggedIn("You are already logged in now")
			if r.status_code == 406:
				raise UsernameAlreadyTaken("This username is already taken")

	def login(self, username, password):
		r = self.session.get(url=self.api_login, auth=HTTPBasicAuth(username, password))
		result = r.json()

		if not result["ok"]:
			if r.status_code == 403:
				raise InvalidLoginOrPassword()
		elif result["ok"] and "message" in result:
			raise AlreadyLoggedIn()

		self.logged_in = True
		return result

	@auth_required
	def logout(self):
		r = self.session.get(url=self.api_logout)
		self.logged_in = False
		return r
