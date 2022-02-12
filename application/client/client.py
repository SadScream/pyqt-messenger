# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime
import secrets
import string

from random import choice
from requests.exceptions import ConnectionError

from PySide2 import QtCore, QtGui, QtWidgets, QtMultimedia

from classes.connection.connection import Connection
from classes.config.config import Config
from classes.config.errors import *
from classes.pulling import Puller

from ui.settings import Settings
from ui.design import Ui_MainWindow

'''
TODO
добавить отправку медиа
'''

# color = choice(['rgb(225, 103, 148)',
# 	'rgb(236, 117, 119)',
# 	'rgb(69, 179, 224)',
# 	'rgb(63, 199, 195)',
# 	'rgb(94, 190, 127)',
# 	'rgb(236, 117, 101)',
# 	'rgb(179, 131, 215)',
# 	'rgb(225, 103, 148)',
# 	'rgb(79, 53, 225)'
# 	])

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
				background-color: rgb(43,82,120);
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
	<span>username now is {1}</span>
</div>'''
# templates


class App(QtWidgets.QMainWindow, Ui_MainWindow):
	EVENT = QtCore.Signal(list)
	ERROR = QtCore.Signal(str)
	PLAY_AUDIO = QtCore.Signal()

	def __init__(self):
		super().__init__()
		self.setupUi(self)

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

		self.config = Config()

		try:
			self.config.load_from_file()
		except FileNotFoundError:
			self.config.password = self.generate_password()
			self.config.upload_to_file()

		self.connection = Connection()
		self.puller = Puller(self.connection, self.puller_event_handler)
		self.settings = Settings(self.connection, self.config)

	def constructor(self):
		print(f"[{self.constructor.__name__}]: setting parameters...", end="")

		self.message.setTabStopDistance(4.0)

		print("setting binds of signals...", end="")
		self.settingButton.triggered.connect(self.generateSettingsWindow)
		self.direct.clicked.connect(self.message_handler)

		self.EVENT.connect(self.on_event)
		self.ERROR.connect(self.info_window)
		self.PLAY_AUDIO.connect(self.play_audio)

		self.settingButton.triggered.emit()

		self.load_messages()

		print(f"[{self.constructor.__name__}]: preparing to show window")
		self.show()

		self.message.setFocus()
		
		# self.chat.verticalScrollBar().setSliderPosition(
		# 	self.chat.verticalScrollBar().maximum())

	def generate_password(self):
		alphabet = string.ascii_letters + string.digits
		password = ''.join(secrets.choice(alphabet) for i in range(12))

		return password

	def generateSettingsWindow(self):
		print(f"[{self.generateSettingsWindow.__name__}]: preparing to create `Settings` window")
		self.settings.exec_()
		print("...`Settings` window closed. ", end='')

		if not self.puller.serve:
			print("Start pulling")
			self.puller.start_pulling()
		else:
			print("")

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
		self.show_message.setIcon(QtWidgets.QMessageBox.Warning)
		self.show_message.setText(text)
		self.show_message.setWindowTitle("Ошибка")

		ok = self.show_message.exec_()
	
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
					msg = msg[:512]

				self.connection.send_message(msg, date=time.time())
				self.message.setFocus()

	def load_messages(self):
		'''
		загрузка истории сообщений при старте приложения
		'''

		self.puller.pull_once()

	def puller_event_handler(self, data):
		if isinstance(data, list):
			self.EVENT.emit(data)
		elif isinstance(data, Exception):
			self.ERROR.emit("Ошибка соединения с сервером")

	@QtCore.Slot(list)
	def on_event(self, events):
		for event in events:
			if event["type"] == "messages":
				self.process_message(event)
			elif event["type"] == "usernames":
				self.process_username(event)
			elif event["type"] == "connections":
				self.process_connection(event)

	def process_message(self, event):
		text = event["text"]
		name = event["username"]
		time_ = self.time(event["date"])

		l = len(text + time_)
		width = l * 9

		if width > 300:
			width = 290

		if event["owner_id"] == self.config.user_id:
			template = message_to.format(width, text, time_)
		else:
			template = message_from.format(width, "rgb(225, 103, 148)", name, text, time_)

		self.chat.text_chat = template + self.chat.text_chat

	def process_username(self, event):
		if self.config.user_id == event["user_id"]:
			old_name = "Your"
			new_name = event["new_username"]
		else:
			old_name = event["old_username"]
			new_name = event["new_username"]

		self.chat.text_chat = nick_template.format(old_name, new_name) + self.chat.text_chat

	def process_connection(self, event):
		text = "connected." if event["is_connected"] else "disconnected."

		if self.config.user_id == event["user_id"]:
			name = "You are"
		else:
			name = event["username"]

		self.chat.text_chat = connection_template.format(name, text) + self.chat.text_chat

	def closeEvent(self, evnt):
		'''
		вызывается при закрытии окна
		'''

		print(f"[{self.closeEvent.__name__}]: close event discovered. Exiting...", end=" ")

		self.config.upload_to_file()
		self.puller.stop_pulling()

		try:
			self.connection.logout()
		except ConnectionError:
			pass

		print("Exited")
		evnt.accept()


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = App()
	window.constructor()
	app.exec_()