import requests, threading


class Server:
	def __init__(self, window):
		self.window = window
		self.respond = False
		self.handler_is_on = True
		self.host = None
		self._th = None

		self._requests = []

		self.data = []

		self.methods = [
                    "user.getUsernames",
					"user.check", "user.getid",
                	"user.connect", "user.disconnect",
					"user.rename", 
					"events.get", "events.getAll",
					"messages.send"
					]
	
	def init(self, host):
		self.respond = False
		self.window.connection_established = False

		self.host = self._host_to_url(host)
		valid = self._check_host()

		if not valid:
			raise Exception("Invalid host or server doesn't respond")
		else:
			self.respond = True
			self._th = threading.Thread(target=self.request_handler)
			self._th.start()
			print("Host is valid!")
	
	def request_handler(self):
		while self.handler_is_on:
			if len(self._requests):
				tmp = self._requests[0]
				self._requests.pop(0)

				f = tmp["method"]
				args = tmp["args"]

				try:
					if len(args) == 2:
						r = f(args[0], json=args[1])
					else:	
						r = f(args)
				except requests.ConnectionError:
					self.respond = False
					self.window.connection_established = False
					self.window.SERVER_ERROR.emit("Connection error")
					raise Exception("[SERVER] Connection error")
				except Exception as E:
					self.respond = False
					self.window.connection_established = False
					self.window.SERVER_ERROR.emit(f"Unknown error while trying to get data - {E}")
					raise Exception(f"[SERVER] Unknown error while trying to get data - {E}")
				
				self.data.append(r.json())
				# print(self.data[-1])

	def method(self, method:str, data:dict = {}):
		if method not in self.methods:
			self.window.SERVER_ERROR.emit("Unknown method")
			raise Exception("[SERVER] Unknown method")
		elif not isinstance(data, dict):
			self.window.SERVER_ERROR.emit("Data param should be a dictionary")
			raise Exception("[SERVER] Data param should be a dictionary")
		
		if data:
			self._requests.append(
				{"method": requests.post, "args": (f"{self.host}/{method}", data)})
		else:
			self._requests.append(
				{"method": requests.get, "args": (f"{self.host}/{method}")})
	
	def get_data(self, event_type=None, request_type=None):
		while True:
			if len(self.data) == 0:
				continue

			data = self.data[0]

			if data and "ok" in data:
				self.data.pop(0)
				continue

			elif data:

				if event_type:
					continue
				if request_type and request_type not in data:
					continue

				self.data.pop(0)
				return data

			elif not data:
				continue

	def get_events(self, after):
		self.method("events.get", {"after": after})
		return self.get_data(request_type="events")

	def get_all_events(self):
		self.method("events.getAll")
		return self.get_data(request_type="allEvents")["allEvents"]
	
	def _check_host(self):
		print(f"[{self._check_host.__name__}]: preparing to check host...", end="")

		try:
			response = requests.post(self.host, json={"key": "_scream_"})
			print("got response...", end="")

			result = response.json()["ok"]
			print("got result...", end="")

			if isinstance(result, bool):
				print("ready.")
				return result
			else:
				print("result isn't an instance of bool!")
				return False
		except:
			print("an exception occured!")
			return False
	
	def _host_to_url(self, host):
		print(f"[{self._host_to_url.__name__}]: going to change host to url...", end="")

		protocol = "http://" if ":5000" in host else "https://"
		print(f"protocol is {protocol}...", end="")

		if "http" not in host[:8]:
			host = protocol + host

		print("output: " + host)
		return host
