import time, hashlib
import socket
import pickle
import json
import threading
from os import listdir

hosted = socket.gethostbyname(socket.gethostname())
print(hosted)
port = 11719

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((hosted,port))
s.listen(3)


print("[ Server Started ]")


class Json_handler:

	def __init__(self):
		listDir = listdir()
		default = {"hashes": []}

		if "SERVER_DATA.json" not in listDir:
			with open("SERVER_DATA.json", "w", encoding='utf-8') as file:
				json.dump(default, file, indent=4, ensure_ascii=False)

	def upload(self, section, key, value=None):
		self.download(section)
		self._upload(section, key, value)

	def download(self, section, key = None):
		with open("SERVER_DATA.json", "r", encoding='utf-8') as file:
			self.data = json.loads(file.read())

			if section == "hashes":
				self.object = self.data[section]

			return self.object

	def _upload(self, section, key, value):
		with open("SERVER_DATA.json", "w", encoding='utf-8') as file:
			if section == "hashes":
				self.data[section].append({key:value})
				json.dump(self.data, file, indent=4, ensure_ascii=False)
			elif section == "nick":
				i=0
				for item in self.data["hashes"]:
					for k, v in item.items():
						if k == value:
							self.data["hashes"].remove(self.data["hashes"][i])
							self.data["hashes"].append({key:v})
							break
						else:
							i+=1
				json.dump(self.data, file, indent=4, ensure_ascii=False)


class Main(Json_handler):
	def __init__(self):
		super().__init__()
		self.quit = False
		self.clients = []
		self.threads = []

		th = threading.Thread(target=self.connection_handler, args=(s,))
		th.start()
		self.error_catcher()

	def error_catcher(self):
		try:
			while True:
				continue

		except KeyboardInterrupt:
			self.quit = True
			s.close()

	def connection_handler(self, sock):
		while True:
			if self.quit:
				break

			try:
				client, addr = sock.accept()
				print(f"Connection with {addr} established.", end=" ")
			except:
				return

			if client not in self.clients:
				print("Adding new client")
				self.clients.append(client)
				self.threads.append([threading.Thread(target=self.sender_handler, args=(client, addr)), client])
				self.threads[-1][0].start()
				# print(f"\n[{self.connection_handler.__name__}] new client added\nclient: {self.clients}\nthreads: {self.threads}\n")
				
	def sender_handler(self, client, addr):
		try:
			while True:
				if self.quit:
					break

				event = pickle.loads(client.recv(4096)) # ждем отправки на сервер пакетов
				
				itsatime = time.strftime("%Y-%m-%d. . .%H:%M:%S", time.localtime())
				info = (f"[{addr[0]}]=[{str(addr[1])}]=[{itsatime}]")

				if event[0] == "`CONFIRM_CONNECTION`":
					for user in self.clients:
						if user == client:
							loaded = ["`CONFIRMED`"]
							user.send(pickle.dumps(loaded))
							break			

				elif event[0] == "CONNECTED":
					print(info + "/user_connected")

					for user in self.clients:
						if user == client:
							loaded = [event[0], "[You are connected.]"]
						elif user != client:
							loaded = [event[0], f"[{event[1]} connected.]"]

						user.send(pickle.dumps(loaded))


				elif event[0] == "DISCONNECTED":
					print(info + "/user_disconnected")

					for user in self.clients:
						if user != client and event[1] != "":
							loaded = [event[0], f"[{event[1]} disconnected.]"]
							# user.send(pickle.dumps(loaded))
						elif user == client:
							loaded = [event[0], f"[SELF]"]

						user.send(pickle.dumps(loaded))
					
					# index = 0

					# for (i, item) in enumerate(self.clients):
					# 	if item[1] == client:
					# 		index = i
					# 		break

					index = self.clients.index(client)

					self.clients.pop(index)
					self.threads.pop(index)
					return


				elif event[0] == "NICK_CHANGED":
					print(info + "/shanged_nick")

					found = self.searchNickname(event[3], event[4])

					if found == False:
						super().upload("nick", event[3], event[2])

						for user in self.clients:
							if user == client:
								loaded = [event[0],
											f"[{event[1]}]  [Your nickname now is {event[3]}]",
											True]

							elif user != client and event[2] != "":
								loaded = [event[0],
											f"[{event[1]}]  [{event[2]} nickname now is {event[3]}]",
											None]

							user.send(pickle.dumps(loaded))
					else:
						for user in self.clients:
							if user == client:
								user.send(pickle.dumps([event[0], "", False]))


				elif event[0] == "GET_HASH":
					generated = str(hashlib.md5((str(addr)+str(event[2])).encode("utf-8")).hexdigest())
					client.send(pickle.dumps([event[0], generated]))
					super().upload("hashes", event[1], generated)


				elif event[0] == "CHECK_HASH":
					users_hash = super().download("hashes")
					confirmed = False

					for item in users_hash:
						if confirmed:
							break

						for k, v in item.items():
							if v == event[1]:
								confirmed = True
								break

					if confirmed:
						client.send(pickle.dumps([event[0], "CONFIRMED"]))
					else:
						client.send(pickle.dumps([event[0], "UNCONFIRMED"]))


				elif event[0] == "MESSAGE":
					print(info + "/new_message")

					for user in self.clients:
						if user != client:
							loaded = [event[0], f"[{event[1]}]  {event[2]}: {event[3]}"]
						elif user == client:
							loaded = [event[0], f"[{event[1]}]  You: {event[3]}"]
						
						user.send(pickle.dumps(loaded))
		except:
			return


	def searchNickname(self, toCheck, user_hash): # потом
		'''
		возвращаемые значения:
		true: если никнейм уже принадлежит другому пользователю
		false: в ином случае
		'''

		loading = super().download("hashes")

		for n in loading:
			for k, v in n.items():
				if k == toCheck and v != user_hash:
					return True

		return False

if __name__ == '__main__':
	Main()