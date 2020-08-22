# -*- coding: utf-8 -*-

from extra import fix_qt_import_error
from extra import config_handler

import os
import sys
import pickle

from PySide2 import QtCore, QtGui, QtWidgets
from time import strftime, localtime, sleep

from extra.connection import *
from ui.settings import Settings
from ui.design import Ui_MainWindow
from ui import res_rc


CONNECT =    "CONNECTED"
DISCONNECT = "DISCONNECTED"
NICK =       "NICK_CHANGED"
GET =        "GET_HASH"
CHECK =      "CHECK_HASH"
MSG =        "MESSAGE"


class App(QtWidgets.QMainWindow, Ui_MainWindow):
	HASH_SIGNAL = QtCore.Signal()

	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.HASH_UNCONFIRMED = False
		self.NICK_EXISTS = None

		self.sock = Connection()
		self.settings = Settings(self, config)

		self.listening_active = False
		self.th = None


	def constructor(self):
		print(f"[{self.constructor.__name__}]: setting parameters...", end="")

		self.message.setTabStopDistance(4.0)

		print("reading config...", end="")
		self.read_config()

		print("filling the fields...", end="")
		self.settings.fields_filler(self.nickname, self.server_ip) # class

		print("setting binds of signals...", end="")
		self.settingButton.triggered.connect(self.generateSettingsWindow) # button
		self.HASH_SIGNAL.connect(self.info_window)
		self.direct.clicked.connect(self.message_handler)

		print("checking of `first_time` parameter...")
		first_time = config.read("first_time")
		print(f"[{self.constructor.__name__}]: first_time = {first_time}")


		if first_time:
			self.settingButton.triggered.emit()
			config.write("first_time", False)
		else:
			status = try_to_connect(window, self.server_ip)

			if not status:
				self.settingButton.triggered.emit()


		print(f"[{self.constructor.__name__}]: preparing to get/check user hash")
		self.hash_handler(self.hash)
		self.message.setFocus()

		print(f"[{self.constructor.__name__}]: preparing to show window")
		self.show()


	def generateSettingsWindow(self):
		print(f"[{self.generateSettingsWindow.__name__}]: preparing to create `Settings` window")
		self.settings.valid_settings = None
		self.settings.exec_()

		print(f"[{self.generateSettingsWindow.__name__}]: self.settings.valid_settings = {self.settings.valid_settings}")

		if self.settings.valid_settings == False:
			self.generateSettingsWindow()


	def read_config(self, nickname = False, hash_ = False, ip = False):
		'''
		читаем либо что-то конкретное из файла конфига, либо все сразу
		'''

		if nickname:
			self.nickname = config.read("nickname")
		if hash_:
			self.hash = config.read("hash")
		if ip:
			self.server_ip = config.read("ip")

		elif not nickname and not hash_ and not ip:
			self.nickname = config.read("nickname")
			self.hash = config.read("hash")
			self.server_ip = config.read("ip")


	def time(self):
		return strftime("%H:%M:%S", localtime())


	def info_window(self, text_ = False):
		'''
		вызов окна с определенным сообщением
		'''

		text = ""

		if not text_:
			if self.HASH_UNCONFIRMED:
				text = "Invalid user"
		else:
			text = text_

		self.show_message = QtWidgets.QMessageBox(self)

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/icons/icons/chat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.show_message.setWindowIcon(icon)
		self.show_message.setIcon(QtWidgets.QMessageBox.Information)
		self.show_message.setText(text)
		self.show_message.setWindowTitle("Информация")

		ok = self.show_message.exec_()

		if ok and self.HASH_UNCONFIRMED:
			print(f"[{self.info_window.__name__}]: hash UNCONFIRMED.")

			if self.sock.connected():
				self.send(DISCONNECT, self.nickname)
				print(f"[{self.info_window.__name__}]: closing socket...", end="")

				while self.listening_active:
					continue

				self.sock.close_socket()
				print("closed")

			print(f"[{self.info_window.__name__}]: closing application.")
			self.close()


	def hash_handler(self, arg):
		'''
		получение/проверка хэша
		'''

		if arg == "new":
			self.send(GET, self.nickname, self.time())
		else:
			self.send(CHECK, self.hash)


	def closeEvent(self, evnt):
		'''
		вызывается при закрытии окна
		'''

		print(f"[{self.closeEvent.__name__}]: close event discovered. Exiting...", end=" ")

		if not self.HASH_UNCONFIRMED:
			print("Closing socket...", end="")

			self.send(DISCONNECT, self.nickname)

			while (self.listening_active):
				continue
			
			self.sock.close_socket()
			print("closed.")

		config.close()
		print("Exited")
		evnt.accept()


	def message_handler(self):
		'''
		функция для отправки сообщений
		'''
		
		self.msg = self.message.toPlainText()

		if not (self.msg.isspace()):
			if len(self.msg) > 0:
				print(f"[{self.message_handler.__name__}]: trying to send message...", end="")

				self.message.clear()
				self.send(MSG, self.time(), self.nickname, self.msg)
				self.message.setFocus()

				print(f"message sent")


	def send(self, *sequence):
		'''
		отправка пакетов сокету
		'''

		self.sock.send(pickle.dumps([var for var in sequence]))


	def listen_server(self):
		'''
		ожидание новых пакетов от сервера
		'''

		print(f"[{self.listen_server.__name__}]: start to listening server...")
		self.listening_active = True

		while self.listening_active:
			try:
				data = pickle.loads(self.sock.recv(512))

				# print(f"[{self.listen_server.__name__}]: recieved data `{data[0]}`")

				if data[0] == GET:
					self.send(CONNECT, self.nickname)
					print(f"[{self.listen_server.__name__}]: got new hash.\tHASH: `{data[1]}`")
					config.write("hash", data[1])

				elif data[0] == CHECK:
					print(f"[{self.listen_server.__name__}]: getting hash results...")
					if data[1] == "CONFIRMED":
						print(f"[{self.listen_server.__name__}]: hash confirmed.\tHASH: `{self.hash}`")
						self.send(CONNECT, self.nickname)
						
					elif data[1] == "UNCONFIRMED":
						self.HASH_UNCONFIRMED = True
						self.HASH_SIGNAL.emit()

				elif data[0] == NICK:
					if data[2] == True:
						config.write("nickname", self.settings.nicknameLine.text())
						self.read_config()
						self.NICK_EXISTS = False
						self.chat.append(data[1])
					elif data[2] == False:
						self.NICK_EXISTS = True
					else:
						self.chat.append(data[1])

				elif data[0] == DISCONNECT:
					if data[1] == "[SELF]":
						self.listening_active = False
					else:
						self.chat.append(data[1])

				elif data[0] in [MSG, CONNECT]:
					self.chat.append(data[1])

			except Exception as E:
				print(f"\n[EXCEPTION AT '{self.listen_server.__name__}']: while trying to recieve data `{E}`\n")

				if ("[WinError 10053]" not in str(E)):
					self.chat.append(f"ERROR: {E}")

				self.listening_active = False


if __name__ == '__main__':
	config = config_handler.Config(os.path.join(os.getcwd(), "config.json"))

	app = QtWidgets.QApplication(sys.argv)
	window = App()
	window.constructor()
	app.exec_()