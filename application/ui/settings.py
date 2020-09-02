import sys

from PySide2 import QtCore, QtGui, QtWidgets
from threading import Thread

try:
	from . import res_rc
except ImportError:
	import res_rc


CONNECT =     "user.connect"
DISCONNECT =  "user.disconnect"
NICK_CHANGE = "user.rename"
NICK_SET =    "user.setname"
GET_ID =      "user.getid"
CHECK =       "user.check"
MSG =         "messages.send"


class Ui_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(410, 140)
		Dialog.setMinimumSize(QtCore.QSize(410, 140))
		Dialog.setMaximumSize(QtCore.QSize(410, 140))
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/menuBar/icons/settings.png"),
					   QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
		self.generalForm.setWidget(
			0, QtWidgets.QFormLayout.LabelRole, self.nicknameLabel)
		self.nicknameLine = QtWidgets.QLineEdit(self.formLayoutWidget)
		self.nicknameLine.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
		self.nicknameLine.setAcceptDrops(False)
		self.nicknameLine.setInputMethodHints(QtCore.Qt.ImhLatinOnly)
		self.nicknameLine.setMaxLength(13)
		self.nicknameLine.setPlaceholderText("")
		self.nicknameLine.setClearButtonEnabled(False)
		self.nicknameLine.setObjectName("nicknameLine")
		self.generalForm.setWidget(
			0, QtWidgets.QFormLayout.FieldRole, self.nicknameLine)
		self.hostLabel = QtWidgets.QLabel(self.formLayoutWidget)
		self.hostLabel.setStyleSheet("")
		self.hostLabel.setObjectName("hostLabel")
		self.generalForm.setWidget(
			1, QtWidgets.QFormLayout.LabelRole, self.hostLabel)
		self.hostLine = QtWidgets.QLineEdit(self.formLayoutWidget)
		self.hostLine.setAcceptDrops(False)
		self.hostLine.setInputMethodHints(QtCore.Qt.ImhLatinOnly)
		self.hostLine.setText("")
		self.hostLine.setMaxLength(40)
		self.hostLine.setObjectName("hostLine")
		self.generalForm.setWidget(
			1, QtWidgets.QFormLayout.FieldRole, self.hostLine)
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
		icon1.addPixmap(QtGui.QPixmap(":/icons/icons/loading.png"),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
		self.hostLabel.setText(_translate("Dialog", "Host"))
		self.saveButton.setText(_translate("Dialog", "Save"))
		self.cancelButton.setText(_translate("Dialog", "Cancel"))


class Settings(QtWidgets.QDialog, Ui_Dialog):
	CONNECTION_SIGNAL = QtCore.Signal(bool, str, str)

	def __init__(self, window, server, config):
		super().__init__()
		self.setupUi(self)
		self.loading(False)

		self.INCORRECT_NICKNAME = "Invalid nickname." \
									"Your new nickname should not to: " \
									"consists of spaces, " \
									"been shorter than 3 syms"

		self.NICKNAME_EXISTS = "This nickname alreay taken"
		self.INCORRECT_HOST = "Having trouble trying to connect to specified host"

		self.text = ""
		self.re_open = False

		self.window = window
		self.config = config
		self.server = server

		self.CONNECTION_SIGNAL.connect(self.on_connection)
		self.saveButton.clicked.connect(self.run_)
		self.cancelButton.clicked.connect(self.close_)

	def run_(self):
		'''
		нажата кнопка save
		'''

		self.loading(True)

		self.window.listening_is_on(False)
		thread = Thread(target = self.run_in_thread)
		thread.start()

	def run_in_thread(self):
		name = self.nicknameLine.text()
		host = self.hostLine.text()
		
		is_host_correct = self.check_connect_to_host(host)

		if is_host_correct:
			self.config.write("host", host)
			self.window.read_config(host=True)
		else:
			print("Host isn't correct!")
			return self.CONNECTION_SIGNAL.emit(is_host_correct, name, host)

		print(f'''[{self.run_in_thread.__name__}]: Going to create connection, params:
			  is_host_correct - {is_host_correct}, name - {name}, host - {host}...''')

		return self.CONNECTION_SIGNAL.emit(is_host_correct, name, host)

	def check_connect_to_host(self, host):
		print(f"[{self.check_connect_to_host.__name__}]: going to check connection...", end="")

		if self.server.respond and host == self.config.read("host"):
			print("connected.")
			return True
		elif (self.server.respond and host != self.config.read("host")) or not self.server.respond:
			print("disconnected.")

			try:
				self.server.init(host)
			except:
				self.text = self.INCORRECT_HOST
				return False

			if not self.server.respond:
				self.text = self.INCORRECT_HOST
				return False
			else:
				self.config.write("host", self.server.host)
				self.window.read_config()

			return True

	@QtCore.Slot() # from CONNECTION_SIGNAL
	def on_connection(self, is_host_correct, name, host):
		self.loading(False)

		if not is_host_correct:
			self.window.info_window(self.text)
			self.re_open = True
			return self.close()

		result, self.text = self.name_is_correct(name)

		self.window.listening_is_on(True)

		if result:
			self.config.write("nickname", name)
			self.window.read_config()

			if not self.window.connection_established:
				self.window.connect_to_server()

			return self.close()
		else:
			self.window.info_window(self.text)
			self.re_open = True
			return self.close()

	def name_is_correct(self, name):

		# если имя введено корректно, то проверяем айпи, иначе выходим и говорим пользователю, что нужно исправить имя

		print(f"[{self.name_is_correct.__name__}]: Checking if nickname correct...", end="")

		if not name.isspace() and len(name) > 3 and name != "":
			print("name format correct")
			res_name = self.check_name(name)
		else:
			print("name format isn't correct")
			return (False, self.INCORRECT_NICKNAME)

		if not res_name:
			return (False, self.NICKNAME_EXISTS)
		else:
			return (True, "")

	def check_name(self, name):
		print(f"[{self.check_name.__name__}]: name {'!=' if name != self.config.read('nickname') else '=='} " \
			  f"self.config.read('nickname')...", end="")

		if name != self.config.read("nickname"):
			print("Checking nickname...", end="")

			self.server.method("user.getUsernames")

			result = self.window.get_data("usernames")

			if name in result["usernames"]:
				print("nickname already taken...")
				return False

			if self.config.read("nickname") == "":
				print("OK...", end="")

				self.window.write_signal.emit(
					NICK_CHANGE, "", "Your", f"{name}", "")

				return True
			else:
				self.server.method(NICK_CHANGE, {"id": self.config.read("user_id"), "nickname": name})

		return True

	def close_(self):
		'''
		нажата кнопка cancel
		'''

		if self.window.connection_established:
			self.re_open = False
		else:
			self.re_open = True
		
		self.close()

	def closeEvent(self, evnt):
		'''
		вызывается при знакрытии окна
		'''

		if self.window.connection_established:
			self.nicknameLine.setText(self.config.read("nickname"))
			self.hostLine.setText(self.config.read("host"))
			evnt.accept()
		else:
			if self.re_open:
				self.re_open = False
				evnt.accept()
			else:
				self.window.config.close()
				sys.exit(0)

	def fields_filler(self, name=False, host=False):
		if (not name) and (not host):
			self.nicknameLine.setText("")
			# http://127.0.0.1:5000
			# SadScream.pythonanywhere.com
			self.hostLine.setText("127.0.0.1:5000")
		elif name and (not host):
			self.nicknameLine.setText(name)
		elif (not name) and host:
			self.hostLine.setText(host)
		elif name and host:
			self.nicknameLine.setText(name)
			self.hostLine.setText(host)	

	def loading(self, state):
		'''
		state: True/False
		'''

		if state:
			self.loading_icon.show()
		elif not state:
			self.loading_icon.hide()

		self.saveLayout.setEnabled(not state)
		self.generalBox.setEnabled(not state)
