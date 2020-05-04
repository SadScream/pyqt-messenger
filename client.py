import sys
import socket
import pickle
import res_rc

import fix_qt_import_error
from PyQt5 import QtCore, QtGui, QtWidgets
from time import strftime, localtime, time, sleep
from threading import Thread

import JsonHandler


CONNECT = "CONNECTED"
DISCONNECT = "DISCONNECTED"
NICK = "NICK_CHANGED"
GET = "GET_HASH"
CHECK = "CHECK_HASH"
MSG = "MESSAGE"



# -------------------------------------------------------------------------------
class Ui_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(410, 130)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		Dialog.setWindowIcon(icon)
		self.cancelBox = QtWidgets.QDialogButtonBox(Dialog)
		self.cancelBox.setGeometry(QtCore.QRect(250, 100, 151, 21))
		self.cancelBox.setOrientation(QtCore.Qt.Horizontal)
		self.cancelBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
		self.cancelBox.setObjectName("cancelBox")
		self.generalBox = QtWidgets.QGroupBox(Dialog)
		self.generalBox.setGeometry(QtCore.QRect(10, 10, 391, 81))
		self.generalBox.setStyleSheet("QGroupBox {font-size: 12px;}QLabel {font-size: 13px;}")
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
		self.nicknameLine = NickEdit(self.formLayoutWidget)
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
		self.ipLine.setMaxLength(16)
		self.ipLine.setObjectName("ipLine")
		self.generalForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ipLine)

		self.retranslateUi(Dialog)
		self.cancelBox.accepted.connect(Dialog.accept)
		self.cancelBox.rejected.connect(Dialog.reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("Dialog", "Settings"))
		self.generalBox.setTitle(_translate("Dialog", "General"))
		self.nicknameLabel.setText(_translate("Dialog", "Nickname"))
		self.ipLabel.setText(_translate("Dialog", "Server IP"))


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
		self.setting = QtWidgets.QAction(MainWindow)
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap(":/menuBar/icons/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setting.setIcon(icon3)
		self.setting.setObjectName("setting")
		self.menuSettings.addAction(self.setting)
		self.menuBar.addAction(self.menuSettings.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "SadGram"))
		self.message.setPlaceholderText(_translate("MainWindow", "Enter your message"))
		self.menuSettings.setTitle(_translate("MainWindow", "Menu"))
		self.setting.setText(_translate("MainWindow", "Settings"))
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
		self.cancelBox.accepted.connect(self.run_)
		self.cancelBox.rejected.connect(self.close_)

	def run_(self):
		name = self.nicknameLine.text()
		ip = self.ipLine.text()

		text, result = self.fields_is_correct(name, ip)

		if text:
			self.valid_settings = False
			window.info_window(text)
		else:
			if not result:
				self.valid_settings = False
				window.info_window("Invalid IP or nickname. Remember, your new nickname should not to: " \
																				"consists of spaces, " \
																				"been shorter than 3 syms")
			elif result:
				if name != window.nickname:
					config.write("nickname", self.nicknameLine.text())
					window.send(NICK, window.time(), window.nickname, name)
					window.read_config()
				self.valid_settings = True


	def closeEvent(self, evnt):
		if window.th != None and window.th.is_alive():
			self.nicknameLine.setText(config.read("nickname"))
			self.ipLine.setText(config.read("ip"))
			evnt.accept()
		else:
			return sys.exit(0)


	def close_(self):
		if window.th != None and window.th.is_alive():
			self.nicknameLine.setText(config.read("nickname"))
			self.ipLine.setText(config.read("ip"))
		else:
			self.valid_settings = False


	def fields_is_correct(self, name, ip):
		res_ip = self.check_ip(ip)
		res_name = self.check_name(name)

		if res_ip and res_name:
			return (False, True)

		elif not res_ip and not res_name:
			return (False, False)

		elif res_ip and not res_name:
			return ("Error. Your new nickname should not to: " \
										"consists of spaces, " \
										"been shorter than 3 syms", None)
		
		elif not res_ip and res_name:
			return ("Invalid IP", None)


	def check_ip(self, ip):
		if ip == "127.0.0.1":
			return False
		# elif ip == window.server_ip:
		# 	return True
		else:
			try:
				print(f"[{self.check_ip.__name__}]: sock._closed = {window.sock._closed}")

				if not window.sock._closed:
					try:
						window.send(DISCONNECT, window.nickname)
					except Exception as error:
						print(f"\n[EXCEPTION AT '{self.check_ip.__name__}']: filed to disconnect `{error}`\n")
						pass

					while window.listening_active:
						continue

					window.sock.close()
					window.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

				status = try_to_connect(ip)

				if not status:
					return False

				window.th = Thread(target=window.listen_server, args=(window.sock,))
				window.th.start()

				config.write("nickname", self.nicknameLine.text())
				config.write("ip", ip)

				window.read_config()
				window.hash_handler(window.hash)

				return True

			except Exception as error:
				print(f"\n[EXCEPTION AT '{self.check_ip.__name__}']: presumably failed to start the thread `{error}\n\t`IP `{ip}`\n")

				if ("WinError 10056" in str(error)):
					return True

				return False

	def check_name(self, nickname):
		if not nickname.isspace() and len(nickname) > 3:
			return True
		else:	
			return False

	def fields_filler(self, name="", ip="127.0.0.1"):
		self.nicknameLine.setText(name)
		self.ipLine.setText(ip)


class App(QtWidgets.QMainWindow, Ui_MainWindow):
	HASH_SIGNAL = QtCore.pyqtSignal()
	NICK_SIGNAL = QtCore.pyqtSignal()

	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.listening_active = False
		self.th = None
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.settings = Settings()
		self.HASH_UNCONFIRMED = False
		self.NICK_EXISTS = False


	def constructor(self):
		self.message.setTabStopDistance(4.0)
		self.read_config()

		self.settings.fields_filler(self.nickname, self.server_ip) # class
		self.setting.triggered.connect(self.generateSettingsWindow) # button

		self.HASH_SIGNAL.connect(self.info_window)
		self.NICK_SIGNAL.connect(self.info_window)
		self.direct.clicked.connect(self.message_handler)

		first_time = config.read("first_time")
		# self.th = Thread(target=self.listen_server, args=(self.sock,))

		if first_time:
			self.setting.triggered.emit()
			config.write("first_time", False)
		else:
			status = try_to_connect(self.server_ip)

			if not status:
				self.setting.triggered.emit()

		print(f"[{self.constructor.__name__}]: preparing to get/check hash")
		
		if self.th == None:
			self.th = Thread(target=window.listen_server, args=(window.sock,))
			self.th.start()

		self.hash_handler(self.hash)
		print(f"[{self.constructor.__name__}]: hash confirmed.\tHASH: `{self.hash}`")

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
		читаем либо что-то конкретное, либо все сразу
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
			elif self.NICK_EXISTS:
				text = "This nickname already exists"
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
			self.send(DISCONNECT, self.nickname)
			self.th.join()
			self.sock.close()
			self.close()

		elif ok and self.NICK_EXISTS:
			self.info_window("Nickname already exists")
			self.NICK_EXISTS = False
			self.setting.triggered.emit()

	def hash_handler(self, arg):
		'''
		получение/проверка хэша
		'''

		if arg == "new":
			self.send(GET, self.nickname, self.time())
		else:
			self.send(CHECK, self.hash)

	def closeEvent(self, evnt):
		if not self.HASH_UNCONFIRMED:
			self.send(DISCONNECT, self.nickname)
			# self.th.join()
			self.sock.close()

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
		# if sock == None:
		self.sock.send(pickle.dumps([var for var in sequence])) # s - socket
		# else:
		# 	sock.send(pickle.dumps([var for var in sequence]))

	def listen_server(self, sock):
		print(f"[{self.listen_server.__name__}]: starting to listening server...")
		while True:
			try:
				self.listening_active = True
				# if self.sock != sock:
				# 	self.send(DISCONNECT, self.nickname, sock=sock)
				# 	break

				data = pickle.loads(sock.recv(512))

				print(f"[{self.listen_server.__name__}]: recieved data `{data[0]}`")

				if data[0] == GET:
					self.send(CONNECT, self.nickname)
					config.write("hash", data[1])

				elif data[0] == CHECK:
					if data[1] == "CONFIRMED":
						self.send(CONNECT, self.nickname)
						
					elif data[1] == "UNCONFIRMED":
						self.HASH_UNCONFIRMED = True
						self.HASH_SIGNAL.emit()

				elif data[0] == NICK:
					if data[2] == True: 
						self.chat.append(data[1])
					elif data[2] == False:
						self.NICK_EXISTS = True
						self.NICK_SIGNAL.emit()
					else:
						self.chat.append(data[1])

				elif data[0] == DISCONNECT:
					if data[1] == "[SELF]":
						self.listening_active = False
						break
					else:
						self.chat.append(data[1])

				elif data[0] in [MSG, CONNECT]:
					self.chat.append(data[1])

			except Exception as E:
				print(f"\n[EXCEPTION AT '{self.listen_server.__name__}']: while trying to receive data {E}\n")

				if ("[WinError 10053]" not in str(E)):
					self.chat.append(f"ERROR: {E}")

				self.listening_active = False
				break


def try_to_connect(ip):
	'''
	функция для проверки возможности подключения к указанному пользователем айпи адресу
	если при подключении к сокету и отправке на него ключевого слова `CONFIRM_CONNECTION` в течение 3-х секунд не придет ответа, содержащего ключевое слово`CONFIRMED`
	то айпи адрес считается неверным
	'''

	try:
		print(f"[{try_to_connect.__name__}]: connection")
		window.sock.connect((ip, 11719))
	except Exception as error:
		print(f"\n[EXCEPTION AT '{try_to_connect.__name__}']: while trying to connect to socket `{error}`\n")
		return False

	print(f"[{try_to_connect.__name__}]: connection established vrode")

	sleep(3)
	t0 = time()
	data = None

	print(f"[{try_to_connect.__name__}]: preparing to sent HELLO")
	window.sock.send(pickle.dumps(["`CONFIRM_CONNECTION`"]))
	print(f"[{try_to_connect.__name__}]: HELLO sent. Starting waiting for reply")

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
					return True
		except Exception as E:
			print(f"\n[EXCEPTION AT '{try_to_connect.__name__}']: while trying to recieve data `{E}`\n")
			continue


if __name__ == '__main__':
	config = JsonHandler.JsonHandler()

	app = QtWidgets.QApplication(sys.argv)
	window = App()
	window.constructor()
	sys.exit(app.exec_())