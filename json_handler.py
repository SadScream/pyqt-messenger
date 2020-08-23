from json import loads, dumps
import os


class Json_handler:

	def __init__(self):
		self.default = {
			"users": [],
			"events": []
		}

		self.file = os.path.join(os.getcwd(), "SERVER_DATA.json")
		self.most_user_id:int

		if "SERVER_DATA.json" not in os.listdir(os.getcwd()):
			with open(self.file, "w", encoding='utf-8') as file:
				file.write(dumps(self.default, indent=4, ensure_ascii=False))

		self.open()

	def open(self):
		try:
			with open(self.file, "r", encoding="utf-8") as file:
				self.data = loads(file.read(), encoding="utf-8")
				self.most_user_id = len(self.data["users"])
		except Exception as E:
			raise Exception(f"Exception while tring to load config:\t{E}")

	def close(self):
		try:
			with open(self.file, "w", encoding="utf-8") as file:
				file.write(dumps(self.data, ensure_ascii=False, indent=4))
		except Exception as E:
			raise Exception(f"Exception while trying to close config:\t{E}")

	def read_field(self, field):
		if field in self.data:
			self.close()

			return self.data[field]
		else:
			print(f"[{os.path.split(__file__)[1]} => {self.read_field.__name__}] field `{field}` not in data")
			return False

	def read_username(self, user_id):
		self.close()

		return list(self.data["users"][user_id].values())[0]

	def write_event(self, event):
		self.close()
		self.data["events"].append(event)

	def write_user(self, user_id, nickname):
		self.close()
		self.data["users"].append({user_id: nickname})
		self.most_user_id += 1

	def change_user_nickname(self, user_id, nickname):
		self.close()
		self.data["users"][user_id] = nickname