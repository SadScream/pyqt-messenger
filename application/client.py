# -*- coding: utf-8 -*-

from extra import fix_qt_import_error
from extra import config_handler

import os
import sys
import time
import threading

from PySide2 import QtCore, QtGui, QtWidgets
from time import strftime, localtime, sleep

from extra.connection import Server
from ui.settings import Settings
from ui.design import Ui_MainWindow
from ui import res_rc


CONNECT =    "user.connect"
DISCONNECT = "user.disconnect"
NICK =       "user.rename"
GET_ID =     "user.getid"
CHECK =      "user.check"
MSG =        "messages.send"


class App(QtWidgets.QMainWindow, Ui_MainWindow):
	ID_SIGNAL = QtCore.Signal()
	ERROR = QtCore.Signal(str)

	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.ID_UNCONFIRMED = False

		path_to_cfg = os.path.join(os.getcwd(), "config.json")

		self.config = config_handler.Config(path_to_cfg)
		self.server = Server(self)
		self.settings = Settings(self, self.server, self.config)
		self.connection_established = False

		self.listening_active = False
		self.thread = None

	def constructor(self):
		print(f"[{self.constructor.__name__}]: setting parameters...", end="")

		self.message.setTabStopDistance(4.0)

		print("reading config...", end="")
		self.read_config()

		print("filling the fields...", end="")
		self.settings.fields_filler(self.nickname, self.host) # class

		print("setting binds of signals...", end="")
		self.settingButton.triggered.connect(self.generateSettingsWindow) # button
		self.direct.clicked.connect(self.message_handler)
		self.ID_SIGNAL.connect(lambda: self.info_window("Invalid user"))
		self.ERROR.connect(self.info_window)

		print("checking of `first_time` parameter...")
		first_time = self.config.read("first_time")
		print(f"[{self.constructor.__name__}]: first_time = {first_time}")

		if first_time:
			self.settingButton.triggered.emit()
			self.config.write("first_time", False)
		else:
			if self.host != None:
				try:
					self.server.init(self.host)

					if self.server.connected:
						self.connect_to_server()
				except Exception as E:
					self.info_window(str(E))

				if not self.server.connected:
					self.settingButton.triggered.emit()
			else:
				self.settingButton.triggered.emit()
		
		self.message.setFocus()

		print(f"[{self.constructor.__name__}]: preparing to show window")
		self.show()

	def connect_to_server(self):
		print(f"[{self.connect_to_server.__name__}]: preparing to get/check user id")
		self.user_id_handler(self.user_id)
		self.server.method(CONNECT, {"user_id": self.user_id})
		self.connection_established = True
		self.chat.append("[ You are connected. ]")

		self.thread = threading.Thread(target=self.listen_server)
		self.thread.start()

	def generateSettingsWindow(self):
		print(f"[{self.generateSettingsWindow.__name__}]: preparing to create `Settings` window")
		self.settings.exec_()

		print(f"[{self.generateSettingsWindow.__name__}]: self.connection_established = {self.connection_established}")

		if self.connection_established == False:
			self.generateSettingsWindow()

	def read_config(self, nickname = False, user_id = False, host = False):
		'''
		читаем либо что-то конкретное из файла конфига, либо все сразу
		'''

		if nickname:
			self.nickname = self.config.read("nickname")
		if user_id:
			self.user_id = self.config.read("user_id")
		if host:
			self.host = self.config.read("host")

		elif not nickname and not user_id and not host:
			self.nickname = self.config.read("nickname")
			self.user_id = self.config.read("user_id")
			self.host = self.config.read("host")

	def time(self):
		return strftime("%H:%M:%S", localtime())

	@QtCore.Slot()
	def info_window(self, text = False):
		'''
		вызов окна с определенным сообщением
		'''

		self.show_message = QtWidgets.QMessageBox(self)

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/icons/icons/chat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.show_message.setWindowIcon(icon)
		self.show_message.setIcon(QtWidgets.QMessageBox.Information)
		self.show_message.setText(text)
		self.show_message.setWindowTitle("Информация")

		ok = self.show_message.exec_()

		if ok and self.ID_UNCONFIRMED:
			print(f"[{self.info_window.__name__}]: id UNCONFIRMED.")

			if self.server.connected:
				self.send(DISCONNECT, self.nickname)
				print(f"[{self.info_window.__name__}]: closing connection...", end="")

				while self.listening_active:
					continue

				print("closed")

			print(f"[{self.info_window.__name__}]: closing application.")
			self.close()

	def user_id_handler(self, arg):
		'''
		получение/проверка айди
		'''

		if arg == None:
			response = self.server.method(GET_ID, {"nickname": self.config.read("nickname")})
			self.config.write("user_id", response["user_id"])
			self.read_config(user_id=True)
		else:
			response = self.server.method(CHECK, {"user_id": self.user_id})
			self.ID_UNCONFIRMED = not response["ok"]

			if response["ok"]:
				print("USER_ID confirmed!")
			else:
				print("Invalid user_id")
				self.ID_SIGNAL.emit()
				self.close()

	def closeEvent(self, evnt):
		'''
		вызывается при закрытии окна
		'''

		print(f"[{self.closeEvent.__name__}]: close event discovered. Exiting...", end=" ")

		if not self.ID_UNCONFIRMED:
			print("Closing connection...", end="")

			self.server.method(DISCONNECT, {"user_id": self.user_id})

			while (self.listening_active):
				continue

			print("closed.")

		self.config.close()
		print("Exited")
		evnt.accept()

	def message_handler(self):
		'''
		функция для отправки сообщений
		'''
		
		msg = self.message.toPlainText()

		if not (msg.isspace()):
			if len(msg) > 0:
				print(f"[{self.message_handler.__name__}]: trying to send message...", end="")

				self.message.clear()

				if len(msg) > 512:
					msg = msg[512:]

				self.server.method(MSG, {"message": msg, "user_id": self.user_id})
				self.message.setFocus()
				print(f"message sent")

	def listen_server(self):
		'''
		ожидание новых пакетов от сервера
		'''

		print(f"[{self.listen_server.__name__}]: start to listening server...")
		self.listening_active = True
		after = time.time()

		while self.listening_active:
			try:
				data = self.server.method("events.get", {"after": after})["events"]

				if data:
					data = data[-1]
					after = data["time"]
				else:
					time.sleep(1.33)
					continue
				
				# print(f"[{self.listen_server.__name__}]: recieved data `{data}`")

				if data["type"] == NICK:
					if data["confirmed"] == True:
						if data["user_id"] == self.user_id:
							self.config.write("nickname", data["new_name"])
							self.read_config()
							self.chat.append(f"Your nickname now is {data['new_nam']}")
						else:
							self.chat.append(f"{data['old_name']} set his nickname to {data['new_name']}")
					else:
						self.chat.append(data[1])

				elif data["type"] == DISCONNECT:
					if data["user_id"] == self.user_id:
						self.listening_active = False
					else:
						self.chat.append(f"[ {data['username']} disconnected. ]")

				elif data["type"] == MSG:
					if data["user_id"] == self.user_id:
						self.chat.append(f"You: {data['message']}")
					else:
						self.chat.append(f"{data['username']}: {data['message']}")
				
				elif data["type"] == CONNECT:
					self.chat.append(f"{data['username']} connected.")
				
				time.sleep(0.33)

			except Exception as E:
				print(f"\n[EXCEPTION AT '{self.listen_server.__name__}']: while trying to recieve data `{E}`\n")
				self.listening_active = False
				self.ERROR.emit("[Exception]: "+str(E))


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = App()
	window.constructor()
	app.exec_()
