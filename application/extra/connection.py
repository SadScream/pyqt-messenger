import requests


class Server:
	def __init__(self, window):
		self.window = window
		self.connected = False
		self.host = None

		self.methods = [
                    "user.getUsernames",
					"user.check", "user.getid",
                	"user.connect", "user.disconnect",
					"user.rename", 
					"events.get", "events.getAll",
					"messages.send"
					]
	
	def init(self, host):
		self.connected = False
		self.window.connection_established = False

		self.host = self._host_to_url(host)
		valid = self._check_host()

		if not valid:
			raise Exception("Invalid host or server doesn't respond")
		else:
			self.connected = True
			print("Host is valid!")

	def method(self, method:str, data:dict = {}):
		if method not in self.methods:
			raise Exception("Unknown method")
		elif not isinstance(data, dict):
			raise Exception("Data param should be a dictionary")
		
		try:
			if data:
				response = requests.post(f"{self.host}/{method}", json=data)
			else:
				response = requests.get(f"{self.host}/{method}")
		except requests.ConnectionError:
			self.connected = False
			self.window.connection_established = False
			raise Exception("Connection error")
		except Exception as E:
			self.connected = False
			self.window.connection_established = False
			raise Exception(f"Unknown error while trying to get data - {E}")

		return response.json()
	
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
