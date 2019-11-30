import time, hashlib
import socket
import pickle
import json
import threading

hosted = socket.gethostbyname(socket.gethostname())
print(hosted)
port = 11719

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((hosted,port))
s.listen(3)

print("[ Server Started ]")


class Json_handler:

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
				print(f"Соединение с {addr} установлено")
			except:
				return

			if client not in self.clients:
				self.clients.append(client)
				self.threads.append(threading.Thread(target=self.sender_handler, args=(client, addr)))
				self.threads[-1].start()
				
	def sender_handler(self, client, addr):
		while True:
			if self.quit:
				break

			try:
				event = pickle.loads(client.recv(4096)) # ждем отправки на сервер пакетов
				
				itsatime = time.strftime("%Y-%m-%d. . .%H:%M:%S", time.localtime())
				info = (f"[{addr[0]}]=[{str(addr[1])}]=[{itsatime}]")


				if event[0] == "FLAG_01":
					print(info + "/user_connected")

					for user in self.clients:
						if user == client:
							loaded = ["CONNECTED", "[You are connected.]"]
							user.send(pickle.dumps(loaded))
						elif user != client:
							loaded = ["CONNECTED", f"[{event[1]} connected.]"]
							user.send(pickle.dumps(loaded))


				elif event[0] == "FLAG_02":
					print(info + "/user_disconnected")

					for user in self.clients:
						if user != client:
							loaded = ["DISCONNECTED", f"[{event[1]} disconnected.]"]
							user.send(pickle.dumps(loaded))
						elif user == client:
							loaded = ["DISCONNECTED", f"[SELF]"]
							user.send(pickle.dumps(loaded))

					self.clients.remove(client)


				elif event[0] == "FLAG_03":
					print(info + "/shanged_nick")

					checker = self.searchNickname(event[3])

					if checker:
						super().upload("nick", event[3], event[2])

						for user in self.clients:
							if user == client:
								loaded = ["NICK", f"[{event[1]}]  [Your nickname now is {event[3]}]", checker]
								user.send(pickle.dumps(loaded))
							elif user != client:
								loaded = ["NICK", f"[{event[1]}]  [{event[2]} nickname now is {event[3]}]", None]
								user.send(pickle.dumps(loaded))


				elif event[0] == "FLAG_04":
					generated = str(hashlib.md5((str(addr)+str(event[2])).encode("utf-8")).hexdigest())
					loaded = ["HASH", generated]
					client.send(pickle.dumps(loaded))
					super().upload("hashes", event[1], generated)


				elif event[0] == "FLAG_05":
					users_hash = super().download("hashes")

					is_ok = False
					for item in users_hash:
						for k, v in item.items():
							if v == event[1]:
								loaded = ["HASH_CONFIRMED" , "OK"]
								client.send(pickle.dumps(loaded))
								is_ok = True
					if not is_ok:
						loaded = ["HASH_CONFIRMED", "UNKNOWN"]
						client.send(pickle.dumps(loaded))


				elif event[0] == "FLAG_06":
					print(info + "/new_message")

					for user in self.clients:
						if user != client:
							loaded = ["MESSAGE", f"[{event[1]}]  {event[2]}: {event[3]}"]
							user.send(pickle.dumps(loaded))
						elif user == client:
							loaded = ["MESSAGE", f"[{event[1]}]  You: {event[3]}"]
							user.send(pickle.dumps(loaded))

			except:
				return


	def searchNickname(self, toCheck): # потом
		loading = super().download("hashes")
		nicks = []

		for n in loading:
			for k, v in n.items():
				nicks.append(k)

		for n in nicks:
			if n == toCheck:
				return False

		return True

if __name__ == '__main__':
	Main()