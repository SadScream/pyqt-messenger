import sys
from requests.exceptions import InvalidSchema

from PySide2 import QtCore, QtGui, QtWidgets
from threading import Thread

from classes.connection.errors import * # noqa

try:
	from . import res_rc
except ImportError:
	import res_rc


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
		self.usernameLabel = QtWidgets.QLabel(self.formLayoutWidget)
		self.usernameLabel.setStyleSheet("")
		self.usernameLabel.setObjectName("usernameLabel")
		self.generalForm.setWidget(
			0, QtWidgets.QFormLayout.LabelRole, self.usernameLabel)
		self.usernameLine = QtWidgets.QLineEdit(self.formLayoutWidget)
		self.usernameLine.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
		self.usernameLine.setAcceptDrops(False)
		self.usernameLine.setInputMethodHints(QtCore.Qt.ImhLatinOnly)
		self.usernameLine.setMaxLength(13)
		self.usernameLine.setPlaceholderText("")
		self.usernameLine.setClearButtonEnabled(False)
		self.usernameLine.setObjectName("usernameLine")
		self.generalForm.setWidget(
			0, QtWidgets.QFormLayout.FieldRole, self.usernameLine)
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
		Dialog.setWindowTitle(_translate("Dialog", "Settings")) # noqa
		self.generalBox.setTitle(_translate("Dialog", "General")) # noqa
		self.usernameLabel.setText(_translate("Dialog", "Nickname")) # noqa
		self.hostLabel.setText(_translate("Dialog", "Host")) # noqa
		self.saveButton.setText(_translate("Dialog", "Save")) # noqa
		self.cancelButton.setText(_translate("Dialog", "Cancel")) # noqa


class Settings(QtWidgets.QDialog, Ui_Dialog):
	on_connection_signal = QtCore.Signal()
	on_error_signal = QtCore.Signal(Exception)

	def __init__(self, connection, config):
		super().__init__()
		self.setupUi(self)
		self.loading(False)

		self.config = config
		self.connection = connection

		self.usernameLine.setText(config.username)
		self.hostLine.setText(config.host)

		self.on_connection_signal.connect(self.on_connection)
		self.on_error_signal.connect(self.on_error)
		self.saveButton.clicked.connect(self.run_)
		self.cancelButton.clicked.connect(self.close_)

	def run_(self):
		'''
		нажата кнопка save
		'''

		self.loading(True)

		thread = Thread(target = self.run_in_thread)
		thread.start()

	def run_in_thread(self):
		name: str = self.usernameLine.text()
		host: str = self.hostLine.text()

		if len(name) == 0 or name.isspace() or len(host) == 0 or host.isspace():
			return self.on_error_signal.emit(ValueError())

		try:
			self.connection.set_host(host)
			self.config.host = host
		except ServerUnavailableError as E: # noqa
			return self.on_error_signal.emit(E)
		except InvalidSchema as E: # noqa
			return self.on_error_signal.emit(E)

		if self.connection.logged_in:
			try:
				self.connection.change_nickname(name)
				self.config.username = name
			except UsernameAlreadyTaken as E: # noqa
				return self.on_error_signal.emit(E)
		else:
			if self.config.first_time:
				try:
					self.connection.registration(name, self.config.password)
					result = self.connection.login(name, self.config.password)
					self.config.username = name
					self.config.user_id = result["user_id"]
					self.config.first_time = False
				except UsernameAlreadyTaken as E: # noqa
					return self.on_error_signal.emit(E)
			else:
				try:
					result = self.connection.login(name, self.config.password)
					self.config.username = name
					self.config.user_id = result["user_id"]
				except InvalidLoginOrPassword as E: # noqa
					return self.on_error_signal.emit(E)

		return self.on_connection_signal.emit()

	@QtCore.Slot()
	def on_connection(self):
		self.loading(False)
		self.close()

	@QtCore.Slot()
	def on_error(self, error: Exception):
		show_message = QtWidgets.QMessageBox(self)
		focusing_widget = None

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/icons/icons/chat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		show_message.setWindowIcon(icon)
		show_message.setIcon(QtWidgets.QMessageBox.Warning)
		show_message.setWindowTitle("Ошибка")

		if isinstance(error, ServerUnavailableError): # noqa
			focusing_widget = self.hostLine
			show_message.setText("Сервер недоступен")
		elif isinstance(error, InvalidLoginOrPassword): # noqa
			focusing_widget = self.usernameLine
			show_message.setText("Неверное имя пользователя")
		elif isinstance(error, UsernameAlreadyTaken): # noqa
			focusing_widget = self.usernameLine
			show_message.setText("Имя уже занято")
		elif isinstance(error, InvalidSchema):
			focusing_widget = self.hostLine
			show_message.setText("Не указан протокол (http:// or https://)")
		elif isinstance(error, ValueError):
			show_message.setText("Некорректный ввод")

		ok = show_message.exec_()
		self.loading(False)

		if focusing_widget:
			focusing_widget.setFocus()

	def close_(self):
		'''
		нажата кнопка cancel
		'''

		if not self.connection.logged_in:
			return
		
		self.close()

	def closeEvent(self, evnt):
		'''
		вызывается при знакрытии окна
		'''

		if self.connection.logged_in:
			evnt.accept()
		else:
			sys.exit(0)

	def loading(self, state):
		'''
		state: True/False
		'''

		if state:
			self.loading_icon.show()
		elif not state:
			self.loading_icon.hide()

		self.saveButton.setEnabled(not state)
		self.cancelButton.setEnabled(not state)
		self.generalBox.setEnabled(not state)
