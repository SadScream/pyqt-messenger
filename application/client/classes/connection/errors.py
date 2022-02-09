class ServerUnavailableError(Exception):
	pass


class RegistrationWhileLoggedIn(Exception):
	pass


class InvalidLoginOrPassword(Exception):
	pass


class AlreadyLoggedIn(Exception):
	pass


class Unauthorized(Exception):
	pass


class UsernameAlreadyTaken(Exception):
	pass


