# -*- coding: utf-8 -*-

from extra import fix_qt_import_error
from extra import config_handler

import os
import sys
import time
from random import choice
import datetime
import threading

from PySide2 import QtCore, QtGui, QtWidgets, QtMultimedia

from extra.connection import Server
from ui.settings import Settings
from ui.design import Ui_MainWindow
from ui import res_rc



'''
TODO
переделать выдачу айдишников
сделать шифрование ивентов
добавить отправку медиа
'''



CONNECT =    "user.connect"
DISCONNECT = "user.disconnect"
NICK =       "user.rename"
GET_ID =     "user.getid"
CHECK =      "user.check"
MSG =        "messages.send"

color = choice(['rgb(225, 103, 148)',
	'rgb(236, 117, 119)',
	'rgb(69, 179, 224)',
	'rgb(63, 199, 195)',
	'rgb(94, 190, 127)',
	'rgb(236, 117, 101)',
	'rgb(179, 131, 215)',
	'rgb(225, 103, 148)',
	'rgb(79, 53, 225)'
	])

## templates
connection_template = '''
<div style="text-align:center;color:rgb(36,42,48);font-size: 11pt;">
	<span>{0}</span>
	<span>{1}</span>
</div>'''

message_to = '''
<div style="padding-top: 1px; padding-bottom: 1px; transform: scaleX(-1);">
	<div style="border: none; padding-top: 3px; 
				padding-bottom: 5px; transform: scaleX(-1);
				background: linear-gradient(21deg, #dd03e4, #5611ec);
				border-radius: 5px; width: {0}px">

		<span style="text-align: left;">
			<div style="color:rgb(245,245,245); padding-left: 6px;">{1}</div>
		</span>

		<span style="text-align: right;">
			<div style="color:rgb(130,141,148); font-size: 9pt; padding-right: 7px;">{2}</div>
		</span>
	</div>
</div>'''

message_from = '''
<div style="padding-top: 1px; padding-bottom: 1px;">
	<div style="border: none; padding-top: 3px; 
				padding-bottom: 5px; background: rgb(51,57,63); 
				border-radius: 5px; width: {0}px">

		<span>
			<div style="color:{1}; padding-left: 8px;">{2}</div>
		</span>

		<span style="">
			<div style="color:rgb(245,245,245); padding-left: 8px;">{3}</div>
		</span>

		<span style="text-align: right;">
			<div style="color:rgb(130,141,148); font-size: 9pt; padding-right: 7px;">{4}</div>
		</span>
	</div>
</div>'''

nick_template = '''
<div style="text-align:center;color:rgb(36,42,48);font-size: 11pt;">
	<span>{0}</span>
	<span>nickname now is {1}</span>
</div>'''
# templates


class App(QtWidgets.QMainWindow, Ui_MainWindow):
	ID_SIGNAL = QtCore.Signal()
	ERROR = QtCore.Signal(str)
	SERVER_ERROR = QtCore.Signal(str)
	PLAY_AUDIO = QtCore.Signal()
	write_signal = QtCore.Signal(str, str, str, str, str)

	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.ID_UNCONFIRMED = False

		path_to_cfg = os.path.join(os.getcwd(), "config.json")
		path_to_file = os.path.abspath(__file__)
		path_to_audio = os.path.join(os.path.split(path_to_file)[0], "audio")
		self.message_audio = None

		print("Search for message sound in:\n")
		print(f"\tpath to file: {os.path.split(path_to_file)[0]}")
		print(f"\tpath to audio: {path_to_audio}...", end="")

		if "audio" in os.listdir(os.path.split(path_to_file)[0]) and "msg.wav" in os.listdir(path_to_audio):
			self.message_audio = QtMultimedia.QSound(os.path.join(path_to_audio, "msg.wav"))
			print("found!")
		else:
			print("NOT found!")

		self.config = config_handler.Config(path_to_cfg)
		self.connection_established = False
		self.listening_active = False
		self.thread = None
		self.paused = False

		self.server = Server(self)
		self.settings = Settings(self, self.server, self.config)

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
		self.SERVER_ERROR.emit(self.info_window)
		self.PLAY_AUDIO.connect(self.play_audio)
		self.write_signal.connect(self.write_chat)

		print("checking of `first_time` parameter...")
		first_time = self.config.read("first_time")
		print(f"[{self.constructor.__name__}]: first_time = {first_time}")

		if first_time:
			self.config.write("first_open_time", time.time())
			self.settingButton.triggered.emit()
			self.config.write("first_time", False)
		else:
			if self.host != None:
				try:
					self.server.init(self.host)

					if self.server.respond:
						self.connect_to_server()
				except Exception as E:
					self.info_window(str(E))

				if not self.server.respond:
					self.settingButton.triggered.emit()
			else:
				self.settingButton.triggered.emit()

		print(f"[{self.constructor.__name__}]: preparing to show window")
		self.show()

		self.message.setFocus()
		
		# self.chat.verticalScrollBar().setSliderPosition(
		# 	self.chat.verticalScrollBar().maximum())

	def connect_to_server(self):
		print(f"[{self.connect_to_server.__name__}]: establishing connection, preparing to get/check user id")
		self.user_id_handler(self.user_id)
		self.server.method(CONNECT, {"user_id": self.user_id})

		self.load_messages()
		self.connection_established = True

		self.thread = threading.Thread(target=self.listen_server)
		self.thread.start()

	def generateSettingsWindow(self):
		print(f"[{self.generateSettingsWindow.__name__}]: preparing to create `Settings` window")
		self.settings.exec_()

		print(f"[{self.generateSettingsWindow.__name__}]: self.connection_established = {self.connection_established}...self.settings.text = {self.settings.text}")

		if self.connection_established == False or self.settings.text == self.settings.NICKNAME_EXISTS:
			self.settings.text = ""
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

	def time(self, float_time):
		t = datetime.datetime.fromtimestamp(float_time)
		return t.strftime('%H:%M')

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

			if self.server.respond:
				self.send(DISCONNECT, self.nickname)
				print(f"[{self.info_window.__name__}]: closing connection...", end="")

				while self.listening_active:
					continue

				print("closed")

			print(f"[{self.info_window.__name__}]: closing application.")
			self.close()
	
	def get_data(self, method):
		while True:
			data = self.server.get_data()

			if method not in data:
				continue
			else:
				return data

	def user_id_handler(self, arg):
		'''
		получение/проверка айди
		'''

		if arg == None:
			self.server.method(GET_ID, {"nickname": self.config.read("nickname")})

			data = self.get_data(GET_ID)

			self.config.write("user_id", data["user_id"])
			self.read_config(user_id=True)
		else:
			self.server.method(CHECK, {"user_id": self.user_id})

			data = self.get_data(CHECK)

			self.ID_UNCONFIRMED = not data["confirmed"]

			if data["confirmed"]:
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

			print("sending disconnect message...", end="")
			disconnect_thread = threading.Thread(
				target=self.server.method, args=(DISCONNECT, {"user_id": self.user_id}))
			disconnect_thread.start()
			print("sent...", end="")

			t = time.time()

			while (self.listening_active):
				if time.time() - t > 5:
					break

				continue

			print("closed.")

		self.config.close()
		self.server.handler_is_on = False
		print("Exited")
		evnt.accept()
	
	def play_audio(self):
		if self.message_audio.isFinished():
			self.message_audio.play()

	def message_handler(self):
		'''
		функция для отправки сообщений
		'''
		
		msg = self.message.toPlainText()

		if not (msg.isspace()):
			if len(msg) > 0:
				self.message.clear()

				if len(msg) > 512:
					msg = msg[512:]

				self.server.method(MSG, {"message": msg, "user_id": self.user_id, "color": color})

				time.sleep(0.3)
				self.message.setFocus()
	
	@QtCore.Slot(str, str, str, str, str)
	def write_chat(self, type_, time_, name, text, color_):	
		if type_ == CONNECT or type_ == DISCONNECT:
			connection_template.format(name, text)

			self.chat.text_chat = connection_template.format(name, text) + self.chat.text_chat

		if type_ == MSG:
			l = len(text + time_)
			width = l * 9
				
			if width > 300:
				width = 290

			if name == "You":
				template = message_to.format(width, text, time_)
			else:
				if l < len(name)+1:
					width = (len(name)+1) * 9

				template = message_from.format(width, color_, name, text, time_)

			self.chat.text_chat = template + self.chat.text_chat
		
		if type_ == NICK:
			self.chat.text_chat = nick_template.format(name, text) + self.chat.text_chat

	def load_messages(self):
		after = self.config.read("first_open_time")
		self.server.method("events.getAll")

		data = self.get_data("allEvents")
			
		data_events = data["allEvents"]

		if data_events:
			for data in data_events:
				self.processing_data(data, on_loading=True, after=after)

	def listening_is_on(self, status):
		self.paused = not status

	def listen_server(self):
		'''
		ожидание новых пакетов от сервера
		'''

		print(f"[{self.listen_server.__name__}]: start to listening server...")
		self.listening_active = True
		after = time.time()

		while self.listening_active:
			try:
				if self.paused:
					continue

				self.server.method("events.get", {"after": after})

				_data = self.server.get_data()

				if "events" in _data:
					if not len(_data["events"]):
						time.sleep(0.34)
						continue

					data = _data["events"][-1]
					after = data["time"]
				else:
					time.sleep(0.34)
					continue
				
				# print(f"[{self.listen_server.__name__}]: recieved data `{data}`")

				self.processing_data(data)

			except Exception as E:
				print(f"\n[EXCEPTION AT '{self.listen_server.__name__}']: while trying to recieve data `{E}`\n")
				self.listening_active = False

				if "[SERVER]" not in str(E):
					self.ERROR.emit("[Exception]: "+str(E))

	def processing_data(self, data, on_loading = False, after=None):
		if on_loading:
			if not data["time"] > after:
				return

		if data["type"] == NICK:
			if data["user_id"] == self.user_id:
				self.config.write("nickname", data["new_name"])
				self.read_config()
				self.write_signal.emit(NICK, "", "Your", f"{data['new_name']}", "")
			else:
				self.write_signal.emit(NICK, "", f"{data['old_name']}", f"{data['new_name']}", "")

		elif data["type"] == DISCONNECT:
			if data["user_id"] == self.user_id and not on_loading:
				self.listening_active = False
			elif data["user_id"] != self.user_id:
				self.write_signal.emit(data["type"], "", data['username'], "disconnected", "")
			elif data["user_id"] == self.user_id and on_loading:
				self.write_signal.emit(data["type"], "", "You are", "disconnected", "")

		elif data["type"] == MSG:
			if data["user_id"] == self.user_id:
				self.write_signal.emit(data["type"], self.time(data['time']), "You", data['message'], "")
			else:
				if self.message_audio != None and not on_loading:
					self.PLAY_AUDIO.emit()
					
				self.write_signal.emit(data["type"], self.time(data['time']), data['username'], data['message'], data['color'])
		
		elif data["type"] == CONNECT:
			if data["user_id"] != self.user_id:
				self.write_signal.emit(data["type"], "", data['username'], "connected", "")
			if data["user_id"] == self.user_id:
				self.write_signal.emit(data["type"], "", "You are", "connected", "")
		
		if not on_loading:
			time.sleep(0.34)
		else:
			return


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = App()
	window.constructor()
	app.exec_()