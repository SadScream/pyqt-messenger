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
			self.write_def_data()
		else:
			self.open()

	def write_def_data(self):
		with open(self.file, "w", encoding='utf-8') as file:
			file.write(dumps(self.default, indent=4, ensure_ascii=False))
		
		self.open()

	def open(self):
		wrong = False

		try:
			with open(self.file, "r", encoding="utf-8") as file:
				s = file.read()

				if len(str(s)) > 5:
					self.data = loads(s, encoding="utf-8")
					self.most_user_id = len(self.data["users"])
				else:
					wrong = True
		except Exception as E:
			raise Exception(f"Exception while tring to load config:\t{E}")
		
		if wrong:
			return self.write_def_data()

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
		if len(self.data["events"]) > 100:
			print(len(self.data["events"]))
			# если кол-во events больше 100, то 50 первых удаляются
			for i in range((len(self.data["events"])-50)):
				self.data["events"].pop(i)
				
		self.close()
		self.data["events"].append(event)

	def write_user(self, user_id, nickname):
		self.close()
		self.data["users"].append({user_id: nickname})
		self.most_user_id += 1

	def change_user_nickname(self, user_id, nickname):
		self.close()

		self.data["users"][user_id] = {f"{user_id}": nickname}
		
		self.close()
