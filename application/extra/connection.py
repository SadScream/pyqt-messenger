from time import sleep, time
from threading import Thread

import pickle
import socket


class Connection:

	def __init__(self, ip = False, port = False):
		self.ip = ip
		self.port = 11719

		if port:
			self.port = port

		self.closed = True
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def recv(self, data):
		return self.sock.recv(data)

	def send(self, data):
		self.sock.send(data)

	def connected(self):
		return not self.closed

	def close_socket(self):
		'''
		disconnecting socket
		'''

		self.sock.close()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.closed = True
		return self.sock

	def connection(self, ip = False, port = False):
		if ip:
			self.ip = ip
		if port:
			self.port = port

		self.sock.connect((self.ip, self.port))
		self.closed = False
		return self.sock

	def reconnection(self, ip = False, port = False):
		if not self.closed:
			self.close_socket()

		if ip:
			self.ip = ip
		if port:
			self.port = port

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.ip, self.port))
		self.closed = False
		return self.sock


def try_to_connect(window, ip):
	'''
	функция для проверки возможности подключения к указанному пользователем айпи адресу
	если при подключении к сокету и отправке на него ключевого слова `CONFIRM_CONNECTION` в течение 3-х секунд не придет ответа, содержащего ключевое слово`CONFIRMED`
	то айпи адрес считается неверным
	'''

	try:
		print(f"[{try_to_connect.__name__}]: connecting to socket...", end="")

		if not window.sock.connected():
			window.sock.connection(ip)

	except Exception as error:
		print("exception occured!")
		print(f"\n[EXCEPTION AT '{try_to_connect.__name__}']: while trying to connect to socket `{error}`\n")
		return False

	print(f"connection to socket established successfully!")

	sleep(3)
	t0 = time()
	data = None

	print(f"[{try_to_connect.__name__}]: preparing to sent keyword `CONFIRM_CONNECTION`...", end="")
	window.sock.send(pickle.dumps(["`CONFIRM_CONNECTION`"]))
	print("sent! Start waiting for reply")

	while True:
		t1 = time()

		if ((t1 - t0) > 3):
			print(f"[{try_to_connect.__name__}]: 3 seconds passed, breaking...")
			return False

		try:
			data = pickle.loads(window.sock.recv(512))

			if data:
				if data[0] == "`CONFIRMED`":
					print(f"[{try_to_connect.__name__}]: gettings reply...confirmed")

					# window.sock.send(pickle.dumps(["BREAK"]))
					# window.sock.close_socket()
					print(f"[{try_to_connect.__name__}]: start of server listener thread...", end="")
					window.th = Thread(target=window.listen_server, args=())
					window.th.start()

					return True
		except Exception as E:
			print(f"\n[EXCEPTION AT '{try_to_connect.__name__}']: while trying to recieve reply `{E}`\n")
			continue