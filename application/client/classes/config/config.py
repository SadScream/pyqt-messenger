import os
import pickle

try:
	from errors import *
except ModuleNotFoundError:
	from .errors import *

imported = __name__ != "__main__"


class Config:
	def __init__(self):
		self.user_id: int = 0
		self.username: str = ""
		self.password: str = ""
		self.host: str = "http://127.0.0.1:5000"
		self.first_time: bool = True
		self.__config_name: str = "Config.pickle"

	def __repr__(self):
		data = {
			"user_id": self.user_id,
			"username": self.username,
			"host": self.host
		}
		return str(data)

	def upload_to_file(self, path: str = None):
		if path is None:
			path = self.get_path()
		elif not os.path.exists(path):
			raise PathNotFoundError("Given path doesn't exist")
		elif os.path.isfile(path):
			raise PathIsFileError("Given path should not refer to the file")

		with open(os.path.join(path, self.__config_name), 'wb') as f:
			pickle.dump(self, f)

	def load_from_file(self, path: str = None):
		if path is None:
			path = self.get_path()
		elif not os.path.exists(path):
			raise PathNotFoundError("Given path doesn't exist")
		elif os.path.isfile(path):
			raise PathIsFileError("Given path should not refer to the file")

		file = os.path.join(path, self.__config_name)

		if not os.path.exists(file):
			raise FileNotFoundError("There is no Config.pickle at app directory, call `upload_to_file` firstly")

		with open(file, 'rb') as f:
			obj = pickle.load(f)

		self.set_fields_from_cfg(obj)

	def set_fields_from_cfg(self, config):
		for field in self.vars():
			self.__equal_params(field, config)

	def vars(self):
		_vars = []

		for k, v in self.__dict__.items():
			if "__" not in k:
				_vars.append(k)

		return _vars

	def __equal_params(self, param_name, config):
		if hasattr(config, param_name):
			setattr(self, param_name, getattr(config, param_name))
		else:
			pass

	@staticmethod
	def get_path():
		path_to_folder = os.path.split(os.path.abspath(__name__))[0]

		if imported:
			path = path_to_folder
		else:
			path = os.path.split(path_to_folder)[0]

		return path

	def test(self):
		print(self.vars())


if __name__ == "__main__":
	cfg = Config()
	cfg.test()
