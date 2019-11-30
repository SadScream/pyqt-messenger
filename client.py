import sys
import socket
import pickle
import res_rc

from PyQt5 import QtCore, QtGui, QtWidgets
from time import strftime, localtime
from threading import Thread

import JsonHandler


CONNECTED = "FLAG_01"
DISCONNECTED = "FLAG_02"
NICK_CHANGED = "FLAG_03"
GET_HASH = "FLAG_04"
CHECK_HASH = "FLAG_05"
MESSAGE = "FLAG_06"

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

	def __init__(self):
		super().__init__()
		self.setupUi(self)
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

		if self.hash == "new":
			self.hash = self.hash_handler("new")
		else:
			self.hash_handler("confirm")

		if self.nickname != "Client":   
			self.enterNick.insertPlainText(self.nickname)

		self.enterNick.setTabStopDistance(4.0)
		self.message.setTabStopDistance(4.0)

		self.confirmNick.clicked.connect(self.nickname_handler)
		self.direct.clicked.connect(self.message_handler)


	def send(self, *sequence):
		s.send(pickle.dumps([var for var in sequence])) # s - socket


	def time(self):
		return strftime("%H:%M:%S", localtime())


	def hash_handler(self, arg):
		if arg == "new":
			self.send(GET_HASH, self.nickname, self.time())
		elif arg == "confirm":
			self.send(CHECK_HASH, self.hash)


	def closeEvent(self, evnt):
		self.send(DISCONNECTED, self.nickname)
		self.th.join()
		s.close()
		evnt.accept()


	def nickname_handler(self):
		self.new_nickname = self.enterNick.toPlainText()

		if not (self.new_nickname.isspace()):
			if len(self.new_nickname) > 3:
				if self.new_nickname != self.nickname:
					self.send(NICK_CHANGED, self.time(), self.nickname, self.new_nickname)


	def message_handler(self):
		self.msg = self.message.toPlainText()

		if not (self.msg.isspace()):
			if len(self.msg) > 0:
				self.message.clear()
				self.send(MESSAGE, self.time(), self.nickname, self.msg)
				self.message.setFocus()


	def listen_server(self, sock):
		while True:
			try:
				data = pickle.loads(sock.recv(4096))

				if data[0] == "HASH":
					config.write("hash", data[1])

				elif data[0] == "HASH_CONFIRMED":
					if data[1] == "OK":
						self.send(CONNECTED, self.nickname)
					elif data[1] == "UNKNOWN":
						print("unknown")
						self.shutdown = True
						self.th.join() 
						s.close()
						super().closeEvent()                       

				elif data[0] == "NICK":
					if data[2] == True:
						self.nickname = self.new_nickname
						config.write("nickname", self.new_nickname)
					self.chat.append(data[1])

				elif data[0] == "DISCONNECTED":
					if data[1] == "[SELF]":
						break
					else:
						self.chat.append(data[1])

				elif data[0] in list(("MESSAGE", "CONNECTED")):
					self.chat.append(data[1])

			except Exception as E:
				print("1", E)
				self.chat.append(f"ERROR: {E}")


if __name__ == '__main__':
	config = JsonHandler.JsonHandler()

	app = QtWidgets.QApplication(sys.argv)
	window = App()
	sys.exit(app.exec_())