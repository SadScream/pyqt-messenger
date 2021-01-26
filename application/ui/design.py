from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
	QObject, QPoint, QRect, QSize, QSizeF, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
	QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
	QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

from PySide2.QtWebEngineWidgets import QWebEngineView as QWebView, QWebEnginePage, QWebEngineSettings

try:
	from . import res_rc
except ImportError:
	import res_rc


class Chat(QWebView):
	text_chat = property()

	def __init__(self, parent, window):
		self.window = window
		super().__init__(parent)

		self._text = ''
		self.html = ''
		self.text_chat = ''

	def contextMenuEvent(self, e):
		e.ignore()

	@text_chat.getter
	def text_chat(self):
		return self._text
	
	@text_chat.setter
	def text_chat(self, value):
		self._text = value
		self.addHtml()

	def addHtml(self):
		self.html = '''
<!DOCTYPE html>
<html>
	<head>
	<meta charset="utf-8">
	<title>box-sizing</title>
	<style>
		.WRAPPER {
			position: absolute;
			top: 5px;
			left: 4px;
			width: 381px;
			height: 297px;
			padding-left: 10px;
			padding-top: 5px;
			padding-bottom: 5px;
			padding-right: 10px;
			background: rgb(24,25,29);
			border: none;
			border-radius: 6px;
		}

		.main {
			font-family: Calibri;
			font-size: 16px;
			font-weight: 600;
			display: flex;
			flex-direction: column-reverse;
			padding-right: 5px;
			word-wrap: break-word;
			overflow-y: auto;
			overflow-x: hidden;
			scrollbar-width: thin;
			width: 381px;
			height: 297px;
		}

		.main::-webkit-scrollbar {
			width: 8px; /* ширина для вертикального скролла */
			opacity: 1;
		}

		.main::-webkit-scrollbar-track {
			border: none;
			border-radius: 4px;
			background-color: rgb(45,46,48);
		}

		.main::-webkit-scrollbar-thumb {
			/* ползунок  */
			background-color: rgb(88,89,90);
			border-radius: 9em;
		}
	</style>
</head>

<body style="background: rgb(40,46,51);"> 
	<div class="WRAPPER">''' \
		f'''<div class="main">
		{self._text}
		</div>
	</div>
</body>
</html>'''
		self.setHtml(self.html)


class PlainMessage(QPlainTextEdit):
	def __init__(self, parent, window):
		self.window = window
		super().__init__(parent)

	def keyPressEvent(self, e):
		if e.key() == 16777220 and e.modifiers() != Qt.ShiftModifier: # shift+enter
			self.window.message_handler()
		else:
			super().keyPressEvent(e)


'''
		self.chat = Chat(self.centralwidget, self)
		self.chat.setObjectName(u"chat")
		self.chat.setGeometry(QRect(0, 0, 411, 317))
		self.message = PlainMessage(self.centralwidget, self)
'''	


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		if not MainWindow.objectName():
			MainWindow.setObjectName(u"MainWindow")
		MainWindow.resize(410, 410)
		MainWindow.setMinimumSize(QSize(410, 410))
		MainWindow.setMaximumSize(QSize(410, 410))
		icon = QIcon()
		icon.addFile(u":/icons/icons/chat.png",
					 QSize(), QIcon.Normal, QIcon.Off)
		MainWindow.setWindowIcon(icon)
		MainWindow.setStyleSheet(
			u"QMainWindow {background-color: rgb(40,46,51);}")
		self.settingButton = QAction(MainWindow)
		self.settingButton.setObjectName(u"settingButton")
		icon1 = QIcon()
		icon1.addFile(u":/menuBar/icons/settings.png",
					  QSize(), QIcon.Normal, QIcon.Off)
		self.settingButton.setIcon(icon1)
		self.centralwidget = QWidget(MainWindow)
		self.centralwidget.setObjectName(u"centralwidget")
		self.chat = Chat(self.centralwidget, self)
		self.chat.setObjectName(u"chat")
		self.chat.setGeometry(QRect(0, 0, 411, 317))
		self.message = PlainMessage(self.centralwidget, self)
		self.message.setObjectName(u"message")
		self.message.setGeometry(QRect(44, 317, 321, 68))
		self.message.setStyleSheet(
			u"QPlainTextEdit {border: 1px solid rgb(20,26,31);border-radius: 8px;background-color: rgb(40,46,51);color: rgb(245,245,245);font-size:16px;font-family:\"Calibri\";}")
		self.direct = QPushButton(self.centralwidget)
		self.direct.setObjectName(u"direct")
		self.direct.setGeometry(QRect(368, 330, 38, 38))
		self.direct.setStyleSheet(
			u"QPushButton {background-color: rgb(40,46,51);font-size: 13px;border: none;border-radius: 19px;}QPushButton:hover {background-color: rgb(47,53,58);}")
		icon2 = QIcon()
		icon2.addFile(u":/icons/icons/send.png",
					  QSize(), QIcon.Normal, QIcon.Off)
		self.direct.setIcon(icon2)
		self.direct.setIconSize(QSize(48, 48))
		self.attachment = QPushButton(self.centralwidget)
		self.attachment.setObjectName(u"attachment")
		self.attachment.setGeometry(QRect(3, 330, 38, 38))
		self.attachment.setStyleSheet(
			u"QPushButton {background-color: rgb(40,46,51);font-size: 13px;border: none;border-radius: 19px;}QPushButton:hover {background-color: rgb(47,53,58);}")
		icon3 = QIcon()
		icon3.addFile(u":/icons/icons/attachment.png",
					  QSize(), QIcon.Normal, QIcon.Off)
		self.attachment.setIcon(icon3)
		self.attachment.setIconSize(QSize(24, 24))
		MainWindow.setCentralWidget(self.centralwidget)
		self.menuBar = QMenuBar(MainWindow)
		self.menuBar.setObjectName(u"menuBar")
		self.menuBar.setGeometry(QRect(0, 0, 410, 21))
		self.menuSettings = QMenu(self.menuBar)
		self.menuSettings.setObjectName(u"menuSettings")
		MainWindow.setMenuBar(self.menuBar)

		self.menuBar.addAction(self.menuSettings.menuAction())
		self.menuSettings.addAction(self.settingButton)

		self.retranslateUi(MainWindow)

		QMetaObject.connectSlotsByName(MainWindow)
	# setupUi

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(
			QCoreApplication.translate("MainWindow", u"SadGram", None))
		self.settingButton.setText(
			QCoreApplication.translate("MainWindow", u"Settings", None))
		self.message.setPlaceholderText(QCoreApplication.translate(
			"MainWindow", u"Enter your message", None))
		self.direct.setText("")
		self.attachment.setText("")
		self.menuSettings.setTitle(
			QCoreApplication.translate("MainWindow", u"Menu", None))
