# -*- coding: utf-8 -*-

from os import listdir, getcwd
from json import loads, dumps


default = {
    "nickname": "Client",
    "hash": "new"
}


class JsonHandler:

	def __init__(self):
		self.default = default
		self.generateConfig()


	def read(self, field = None):
		with open("DATA.json", "r+", encoding="utf-8") as file:
			data = loads(file.read())

		if field is not None and field in data:
			return data[field]
		else:
			return data


	def write(self, field, value):
		data = self.read()

		if field in data:

			if "**default**" in str(value):
				data[field] = self.default[field]

			else:
				if isinstance(data[field], list):
					if isinstance(value, list):
						data[field] = value
					else:
						data[field].append(value)
				else:
					data[field] = value

			with open("DATA.json", "w", encoding="utf-8") as file:
				file.write(dumps(data, ensure_ascii=False, indent=4))


	def reset(self, field, value):
		data = self.read()

		if field in data:

			if "**default**" in str(value):
				with open("config_copy.json", "w", encoding="utf-8") as file:
					file.write(dumps(data, ensure_ascii=False, indent=4))

				data = self.default

			else:
				if isinstance(data[field], list):
					if isinstance(value, list):
						for value_ in value:
							if value_ in data[field]:
								data[field].remove(value_)
					else:
						if value in data[field]:
							data[field].remove(value)
				else:
					data[field] = value

			with open("DATA.json", "w", encoding="utf-8") as file:
				file.write(dumps(data, ensure_ascii=False, indent=4))


	def generateConfig(self):
		listDir = listdir(getcwd())

		if "DATA.json" not in listDir:	
			with open("DATA.json", "w", encoding="utf-8") as file:
				file.write(dumps(self.default, ensure_ascii=False, indent=4))

		elif "DATA.json" in listDir:
			data = self.read()

			for k, v in self.default.items():
				if k not in data:
					with open("DATA.json", "w", encoding="utf-8") as file:
						file.write(dumps(self.default, ensure_ascii=False, indent=4))
						return