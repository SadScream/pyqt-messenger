import sys
import socket
import pickle
import res_rc

from PyQt5 import QtCore, QtGui, QtWidgets
from time import strftime, localtime
from threading import Thread

import JsonHandler


CONNECT = "CONNECTED"
DISCONNECT = "DISCONNECTED"
NICK = "NICK_CHANGED"
GET = "GET_HASH"
CHECK = "CHECK_HASH"
MSG = "MESSAGE"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.56.1", 11719))


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
		self.enterNick = PlainNickName(self.centralwidget)
		self.enterNick.setGeometry(QtCore.QRect(5, 5, 345, 27))
		self.enterNick.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
		self.enterNick.setAcceptDrops(False)
		self.enterNick.setStyleSheet("QPlainTextEdit {border: none;background: qlineargradient(spread:pad, angle:135, x1:0, y1:0, x2:1, y2:0, stop: 0 rgba(79,98,161,1), stop: 0.65 rgba(155,46,217,1));font-size:16px;font-weight: bold;font-family:\"Calibri\"}")
		self.enterNick.setInputMethodHints(QtCore.Qt.ImhLatinOnly)
		self.enterNick.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.enterNick.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.enterNick.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
		self.enterNick.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
		self.enterNick.setObjectName("enterNick")
		self.confirmNick = QtWidgets.QPushButton(self.centralwidget)
		self.confirmNick.setGeometry(QtCore.QRect(355, 5, 51, 27))
		self.confirmNick.setStyleSheet("QPushButton {background-color: rgb(212, 212, 212);font-size: 13px;border: none;}QPushButton:hover {background-color: rgb(227, 227, 227);}")
		self.confirmNick.setObjectName("confirmNick")
		self.message = PlainMessage(self.centralwidget)
		self.message.setGeometry(QtCore.QRect(5, 350, 361, 54))
		self.message.setStyleSheet("QPlainTextEdit {border: none;background: qlineargradient(spread:pad, angle:135, x1:0, y1:0, x2:1, y2:0, stop: 0 rgba(79,98,161,1), stop: 0.65 rgba(155,46,217,1));font-size:16px;font-family:\"Calibri\";}")
		self.message.setObjectName("message")
		self.direct = QtWidgets.QPushButton(self.centralwidget)
		self.direct.setGeometry(QtCore.QRect(371, 383, 35, 21))
		self.direct.setStyleSheet("QPushButton {background-color: rgb(212, 212, 212);;font-size: 13px;border: none;}QPushButton:hover {background-color: rgb(227, 227, 227);}")
		self.direct.setText("")
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap(":/icons/icons/send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.direct.setIcon(icon1)
		self.direct.setIconSize(QtCore.QSize(33, 33))
		self.direct.setObjectName("direct")
		self.attachment = QtWidgets.QPushButton(self.centralwidget)
		self.attachment.setGeometry(QtCore.QRect(371, 350, 35, 21))
		self.attachment.setStyleSheet("QPushButton {background-color: rgb(212, 212, 212);;font-size: 13px;border: none;}QPushButton:hover {background-color: rgb(227, 227, 227);}")
		self.attachment.setText("")
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap(":/icons/icons/attachment.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.attachment.setIcon(icon2)
		self.attachment.setIconSize(QtCore.QSize(24, 24))
		self.attachment.setObjectName("attachment")
		self.chat = QtWidgets.QTextEdit(self.centralwidget)
		self.chat.setGeometry(QtCore.QRect(5, 38, 401, 307))
		self.chat.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
		self.chat.setStyleSheet("QTextEdit {border: none;background: rgb(245, 245, 245);font-size: 15px;font-family: \"Calibri\"}")
		self.chat.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
		self.chat.setPlaceholderText("")
		self.chat.setObjectName("chat")
		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "SadGram"))
		self.enterNick.setPlaceholderText(_translate("MainWindow", "Enter your nickname"))
		self.confirmNick.setText(_translate("MainWindow", "Accept"))
		self.message.setPlaceholderText(_translate("MainWindow", "Enter your message"))
# --



class PlainNickName(QtWidgets.QPlainTextEdit):

	def __init__(self, parent):
		super().__init__(parent)

	def keyPressEvent(self, e):
		n = 13 # максимальное число символов в строке

		if e.key() == 16777220: # enter
			e.ignore()
		elif e.key() == 86 and e.modifiers() == QtCore.Qt.ControlModifier: # ctrl + v
			super().keyPressEvent(e)
			text = self.toPlainText()
				
			if len(text) >= n:
				self.setPlainText(text[:n])
				self.moveCursor(QtGui.QTextCursor.End)
		else:
			text = self.toPlainText()

			if len(text) >= n and e.text().isalnum():
				self.setPlainText(text[:n])
				self.moveCursor(QtGui.QTextCursor.End)

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


class App(QtWidgets.QMainWindow, Ui_MainWindow):
	SIGNAL = QtCore.pyqtSignal()

	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.HASH_UNCONFIRMED = False
		self.th = Thread(target=self.listen_server, args=(s,))
		self.th.start()

		self.message.setFocus()
		self.constructor()
		self.show()

	def constructor(self):
		self.server_nicknames = []
		self.shutdown = 0
		self.nickname = config.read("nickname")
		self.hash = config.read("hash")
		self.new_nickname = None

		self.hash_handler(self.hash)

		if self.nickname != "Client":
			self.enterNick.insertPlainText(self.nickname)

		self.enterNick.setTabStopDistance(4.0)
		self.message.setTabStopDistance(4.0)

		self.SIGNAL.connect(self.message_)
		self.confirmNick.clicked.connect(self.nickname_handler)
		self.direct.clicked.connect(self.message_handler)


	def send(self, *sequence):
		s.send(pickle.dumps([var for var in sequence])) # s - socket


	def time(self):
		return strftime("%H:%M:%S", localtime())


	def message_(self):
		self.th.join()
		text = ""

		if self.HASH_UNCONFIRMED:
			text = "Invalid user"

		self.show_message = QtWidgets.QMessageBox(self)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/icons/icons/chat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.show_message.setWindowIcon(icon)
		self.show_message.setIcon(QtWidgets.QMessageBox.Information)
		self.show_message.setText(text)
		self.show_message.setWindowTitle("Информация")
		ok = self.show_message.exec_()

		if ok:
			s.close()
			self.destroy()


	def hash_handler(self, arg):
		if arg == "new":
			self.send(GET, self.nickname, self.time())
		else:
			self.send(CHECK, self.hash)


	def closeEvent(self, evnt):
		self.send(DISCONNECT, self.nickname)
		self.th.join()
		s.close()
		evnt.accept()


	def nickname_handler(self):
		self.new_nickname = self.enterNick.toPlainText()

		if not (self.new_nickname.isspace()):
			if len(self.new_nickname) > 3:
				if self.new_nickname != self.nickname:
					self.send(NICK, self.time(), self.nickname, self.new_nickname)


	def message_handler(self):
		self.msg = self.message.toPlainText()

		if not (self.msg.isspace()):
			if len(self.msg) > 0:
				self.message.clear()
				self.send(MSG, self.time(), self.nickname, self.msg)
				self.message.setFocus()


	def listen_server(self, sock):
		while True:
			# try:
			data = pickle.loads(sock.recv(512))

			if data[0] == GET:
				self.send(CONNECT, self.nickname)
				config.write("hash", data[1])

			elif data[0] == CHECK:
				if data[1] == "CONFIRMED":
					self.send(CONNECT, self.nickname)
					
				elif data[1] == "UNCONFIRMED":
					self.HASH_UNCONFIRMED = True
					self.SIGNAL.emit()
					self.send(DISCONNECT, self.nickname)

			elif data[0] == NICK:
				if data[2]:
					self.nickname = self.new_nickname
					config.write("nickname", self.new_nickname)

				self.chat.append(data[1])

			elif data[0] == DISCONNECT:
				if data[1] == "[SELF]":
					break
				else:
					self.chat.append(data[1])

			elif data[0] in [MSG, CONNECT]:
				self.chat.append(data[1])

			# except Exception as E:
			# 	print("1", E)
			# 	self.chat.append(f"ERROR: {E}")


if __name__ == '__main__':
	config = JsonHandler.JsonHandler()

	app = QtWidgets.QApplication(sys.argv)
	window = App()
	sys.exit(app.exec_())