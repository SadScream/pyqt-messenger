import fix_qt_import_error

import res_rc
import JsonHandler

import sys
import pickle

from PyQt5 import QtCore, QtGui, QtWidgets
from time import strftime, localtime, sleep
from threading import Thread

from connection import *


CONNECT =    "CONNECTED"
DISCONNECT = "DISCONNECTED"
NICK =       "NICK_CHANGED"
GET =        "GET_HASH"
CHECK =      "CHECK_HASH"
MSG =        "MESSAGE"



# -------------------------------------------------------------------------------
class Ui_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(410, 140)
		Dialog.setMinimumSize(QtCore.QSize(410, 140))
		Dialog.setMaximumSize(QtCore.QSize(410, 140))
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		Dialog.setWindowIcon(icon)
		self.generalBox = QtWidgets.QGroupBox(Dialog)
		self.generalBox.setGeometry(QtCore.QRect(10, 10, 391, 81))
		self.generalBox.setStyleSheet("QGroupBox {\n"
		"font-size: 12px;\n"
		"}\n"
		"QLabel {\n"
		"font-size: 13px;\n"
		"}")
		self.generalBox.setObjectName("generalBox")
		self.formLayoutWidget = QtWidgets.QWidget(self.generalBox)
		self.formLayoutWidget.setGeometry(QtCore.QRect(9, 20, 201, 48))
		self.formLayoutWidget.setObjectName("formLayoutWidget")
		self.generalForm = QtWidgets.QFormLayout(self.formLayoutWidget)
		self.generalForm.setContentsMargins(0, 0, 0, 0)
		self.generalForm.setObjectName("generalForm")
		self.nicknameLabel = QtWidgets.QLabel(self.formLayoutWidget)
		self.nicknameLabel.setStyleSheet("")
		self.nicknameLabel.setObjectName("nicknameLabel")
		self.generalForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nicknameLabel)
		self.nicknameLine = QtWidgets.QLineEdit(self.formLayoutWidget)
		self.nicknameLine.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
		self.nicknameLine.setAcceptDrops(False)
		self.nicknameLine.setInputMethodHints(QtCore.Qt.ImhLatinOnly)
		self.nicknameLine.setMaxLength(13)
		self.nicknameLine.setPlaceholderText("")
		self.nicknameLine.setClearButtonEnabled(False)
		self.nicknameLine.setObjectName("nicknameLine")
		self.generalForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nicknameLine)
		self.ipLabel = QtWidgets.QLabel(self.formLayoutWidget)
		self.ipLabel.setStyleSheet("")
		self.ipLabel.setObjectName("ipLabel")
		self.generalForm.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.ipLabel)
		self.ipLine = QtWidgets.QLineEdit(self.formLayoutWidget)
		self.ipLine.setAcceptDrops(False)
		self.ipLine.setInputMethodHints(QtCore.Qt.ImhLatinOnly)
		self.ipLine.setText("")
		self.ipLine.setMaxLength(16)
		self.ipLine.setObjectName("ipLine")
		self.generalForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ipLine)
		self.loading_icon = QtWidgets.QPushButton(self.generalBox)
		self.loading_icon.setGeometry(QtCore.QRect(220, 13, 56, 56))
		self.loading_icon.setStyleSheet("QPushButton {\n"
		"background-color: None;\n"
		"border: none;\n"
		"}\n"
		"QPushButton:hover {\n"
		"background-color: None;\n"
		"}")
		self.loading_icon.setText("")
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap(":/icons/icons/loading.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.loading_icon.setIcon(icon1)
		self.loading_icon.setIconSize(QtCore.QSize(64, 64))
		self.loading_icon.setObjectName("loading_icon")
		self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
		self.horizontalLayoutWidget.setGeometry(QtCore.QRect(240, 90, 158, 41))
		self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
		self.saveLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
		self.saveLayout.setContentsMargins(0, 0, 0, 0)
		self.saveLayout.setObjectName("saveLayout")
		self.saveButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.saveButton.setObjectName("saveButton")
		self.saveLayout.addWidget(self.saveButton)
		self.cancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.cancelButton.setObjectName("cancelButton")
		self.saveLayout.addWidget(self.cancelButton)

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("Dialog", "Settings"))
		self.generalBox.setTitle(_translate("Dialog", "General"))
		self.nicknameLabel.setText(_translate("Dialog", "Nickname"))
		self.ipLabel.setText(_translate("Dialog", "Server IP"))
		self.saveButton.setText(_translate("Dialog", "Save"))
		self.cancelButton.setText(_translate("Dialog", "Cancel"))


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(410, 410)
		MainWindow.setMinimumSize(QtCore.QSize(410, 410))
		MainWindow.setMaximumSize(QtCore.QSize(410, 410))
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/icons/icons/chat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		MainWindow.setWindowIcon(icon)
		MainWindow.setStyleSheet("QMainWindow {background-color: rgb(212, 212, 212);}")
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.message = PlainMessage(self.centralwidget)
		self.message.setGeometry(QtCore.QRect(4, 317, 361, 68))
		self.message.setStyleSheet("QPlainTextEdit {border: none;background: qlineargradient(spread:pad, angle:135, x1:0, y1:0, x2:1, y2:0, stop: 0 rgba(79,98,161,1), stop: 0.65 rgba(155,46,217,1));font-size:16px;font-family:\"Calibri\";}")
		self.message.setObjectName("message")
		self.direct = QtWidgets.QPushButton(self.centralwidget)
		self.direct.setGeometry(QtCore.QRect(370, 364, 35, 21))
		self.direct.setStyleSheet("QPushButton {background-color: rgb(212, 212, 212);;font-size: 13px;border: none;}QPushButton:hover {background-color: rgb(227, 227, 227);}")
		self.direct.setText("")
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap(":/icons/icons/send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.direct.setIcon(icon1)
		self.direct.setIconSize(QtCore.QSize(33, 33))
		self.direct.setObjectName("direct")
		self.attachment = QtWidgets.QPushButton(self.centralwidget)
		self.attachment.setGeometry(QtCore.QRect(370, 317, 35, 21))
		self.attachment.setStyleSheet("QPushButton {background-color: rgb(212, 212, 212);;font-size: 13px;border: none;}QPushButton:hover {background-color: rgb(227, 227, 227);}")
		self.attachment.setText("")
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap(":/icons/icons/attachment.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.attachment.setIcon(icon2)
		self.attachment.setIconSize(QtCore.QSize(24, 24))
		self.attachment.setObjectName("attachment")
		self.chat = QtWidgets.QTextEdit(self.centralwidget)
		self.chat.setGeometry(QtCore.QRect(4, 4, 401, 308))
		self.chat.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
		self.chat.setStyleSheet("QTextEdit {border: none;background: rgb(245, 245, 245);font-size: 15px;font-family: \"Calibri\"}")
		self.chat.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
		self.chat.setPlaceholderText("")
		self.chat.setObjectName("chat")
		MainWindow.setCentralWidget(self.centralwidget)
		self.menuBar = QtWidgets.QMenuBar(MainWindow)
		self.menuBar.setGeometry(QtCore.QRect(0, 0, 410, 21))
		self.menuBar.setObjectName("menuBar")
		self.menuSettings = QtWidgets.QMenu(self.menuBar)
		self.menuSettings.setObjectName("menuSettings")
		MainWindow.setMenuBar(self.menuBar)
		self.settingButton = QtWidgets.QAction(MainWindow)
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap(":/menuBar/icons/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.settingButton.setIcon(icon3)
		self.settingButton.setObjectName("setting")
		self.menuSettings.addAction(self.settingButton)
		self.menuBar.addAction(self.menuSettings.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "SadGram"))
		self.message.setPlaceholderText(_translate("MainWindow", "Enter your message"))
		self.menuSettings.setTitle(_translate("MainWindow", "Menu"))
		self.settingButton.setText(_translate("MainWindow", "Settings"))
# -------------------------------------------------------------------------------



class NickEdit(QtWidgets.QLineEdit):

	def __init__(self, parent):
		super().__init__(parent)

	def keyPressEvent(self, e):
		n = 13

		if e.key() == 86 and e.modifiers() == QtCore.Qt.ControlModifier: # ctrl + v
			super().keyPressEvent(e)
			text = self.text()
				
			if len(text) >= n:
				self.setText(text[:n])
				self.setCursorPosition(-1)
		else:
			super().keyPressEvent(e)


class PlainMessage(QtWidgets.QPlainTextEdit):

	def __init__(self, parent):
		super().__init__(parent)

	def keyPressEvent(self, e):
		if e.key() == 16777220 and e.modifiers() != QtCore.Qt.ShiftModifier: # shift+enter
			window.message_handler()
		else:
			super().keyPressEvent(e)



class Settings(QtWidgets.QDialog, Ui_Dialog):

	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.loading(False)

		self.INCORRECT_NICKNAME = "Invalid nickname." \
									"Your new nickname should not to: " \
									"consists of spaces, " \
									"been shorter than 3 syms"

		self.NICKNAME_EXISTS = "This nickname alreay taken"
		self.INCORRECT_IP = "Having trouble trying to connect to specified IP-address"

		self.text = None
		self.artificial_close = False
		self.change_nickname = False # см. функцию check_fields

		self.saveButton.clicked.connect(self.run_)
		self.cancelButton.clicked.connect(self.close_)


	def loading(self, state):
		'''
		state: True/False
		'''

		if state:
			self.loading_icon.show()
			self.saveLayout.setEnabled(False)
			self.generalBox.setEnabled(False)
		elif not state:
			self.loading_icon.hide()
			self.saveLayout.setEnabled(True)
			self.generalBox.setEnabled(True)


	def run_(self):
		'''
		нажата кнопка save
		'''

		self.loading(True)

		thread = Thread(target = self.run_in_thread)
		thread.start()

		while thread.isAlive():
			continue

		self.loading(False)

		if not self.valid_settings:
			window.info_window(self.text)

		self.close()


	def run_in_thread(self):
		name = self.nicknameLine.text() # получаем введенные в поля значения
		ip = self.ipLine.text()

		result, self.text = self.fields_is_correct(name, ip)

		if result:
			self.valid_settings = True

			if ip != window.server_ip:
				config.write("ip", ip)
			
			window.read_config()

			if not window.th.is_alive():
				print(f"[{self.run_in_thread.__name__}]: start of server listener thread...")
				window.th = Thread(target=window.listen_server, args=())
				window.th.start()
		else:
			self.valid_settings = False


	def fields_is_correct(self, name, ip):

		# если имя введено корректно, то проверяем айпи, иначе выходим и говорим пользователю, что нужно исправить имя
		if not name.isspace() and len(name) > 3:
			res_ip, res_name = self.check_fields(ip, name)
		else:
			return (False, self.INCORRECT_NICKNAME)

		# если проверка айпи была пройдена, то идем проверять никнейм, иначе выходим и говорим пользователю, что айпи неверный
		if not res_ip:
			# res_name = self.check_name(name)
			return (False, self.INCORRECT_IP)

		# если айпи и никнейм оказались правильным, то выходим
		if (res_ip and res_name):
			return (True, None)

		# т.к мы уже знаем, что ник введен верно, то в случае, если res_name == False, мы понимаем, что ник уже занят и говорим об этом юзеру 
		elif res_ip and not res_name:
			window.NICK_EXISTS = None
			return (False, self.NICKNAME_EXISTS) # self.NICKNAME_EXISTS


	def check_fields(self, ip, name):
		if (ip == "127.0.0.1"):
			print(f"[{self.check_fields.__name__}]: incorrect IP-address - default")
			return (False, None)

		elif (ip == window.server_ip and window.sock.connected()):
			print(f"[{self.check_fields.__name__}]: already connected to this IP-address")

			if name != window.nickname and name != "":
				print(f"[{self.check_fields.__name__}]: name != window.nickname. Going to change nickname")

				self.change_nickname = True # указываем на то, что пользователь скорее всего вызвал окно настроек, чтобы сменить никнейм

				return (True, self.check_name(name))
			else:
				return (True, True)

		else:
			try:
				print(f"[{self.check_fields.__name__}]: window.sock.connected() = {window.sock.connected()}")

				if window.sock.connected():
					print(f"[{self.check_fields.__name__}]: sending disconnecting message")

					try:
						window.send(DISCONNECT, window.nickname)
					except Exception as error:
						print(f"\n[EXCEPTION AT '{self.check_fields.__name__}']: filed to disconnect `{error}`\n")
						pass

					while (window.listening_active):
						continue
					else:
						window.sock.reconnection(ip)

				status = try_to_connect(window, ip)

				if not status:
					return (False, None)

				print(f"[{self.check_fields.__name__}]: setting new IP for IP field and writing down to config...", end="")
				self.fields_filler(ip=ip)
				print("field set...", end="")
				config.write("ip", ip)
				print("config set.")

				return (True, self.check_name(name))

			except Exception as error:
				print(f"\n[EXCEPTION AT '{self.check_fields.__name__}']: presumably programe failed to start the thread `{error}`\n")

				# if ("WinError 10056" in str(error)):
				# 	return True

				return (False, None)


	def check_name(self, nickname):
		window.send(NICK, window.time(), window.nickname, nickname, window.hash)

		while (window.NICK_EXISTS == None):
			continue
		else:
			if (not window.NICK_EXISTS):
				return True
				self.change_nickname = False
			elif (window.NICK_EXISTS):
				if not self.change_nickname:
					print(f"[{self.check_name.__name__}]: disconnecting. Sending disconnecting message...", end="")
					window.send(DISCONNECT, window.nickname)
					print("sent!")

					while (window.listening_active):
						continue

				self.change_nickname = False
				return False


	def close_(self):
		'''
		нажата кнопка cancel
		'''

		if window.sock.connected():
			self.nicknameLine.setText(config.read("nickname"))
			self.ipLine.setText(config.read("ip"))
		else:
			self.valid_settings = False

		self.close()


	def close(self):
		if not self.artificial_close:
			self.artificial_close = True
			super().close()
		else:
			super().close()


	def closeEvent(self, evnt, artificial = False):
		'''
		вызывается при знакрытии окна
		'''

		if window.sock.connected():
			self.nicknameLine.setText(config.read("nickname"))
			self.ipLine.setText(config.read("ip"))
			evnt.accept()
		else:
			if not self.artificial_close:
				print(f"[{self.closeEvent.__name__}]: close event discovered. Exiting...")
				return sys.exit(0)
			else:
				self.artificial_close = False
				evnt.accept()


	def fields_filler(self, name=False, ip=False):
		if (not name) and (not ip):
			self.nicknameLine.setText("")
			self.ipLine.setText("127.0.0.1")
		elif name and (not ip):
			self.nicknameLine.setText(name)
		elif (not name) and ip:
			self.ipLine.setText(ip)
		elif name and ip:
			self.nicknameLine.setText(name)
			self.ipLine.setText(ip)	



class App(QtWidgets.QMainWindow, Ui_MainWindow):
	HASH_SIGNAL = QtCore.pyqtSignal()

	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.HASH_UNCONFIRMED = False
		self.NICK_EXISTS = None

		self.sock = Connection()
		self.settings = Settings()

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
			print("closed.", end=" ")

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
	config = JsonHandler.JsonHandler()

	app = QtWidgets.QApplication(sys.argv)
	window = App()
	window.constructor()
	sys.exit(app.exec_())