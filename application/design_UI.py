# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

import res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(410, 410)
        MainWindow.setMinimumSize(QSize(410, 410))
        MainWindow.setMaximumSize(QSize(410, 410))
        icon = QIcon()
        icon.addFile(u":/icons/icons/chat.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"QMainWindow {background-color: rgb(212, 212, 212);}")
        self.settingButton = QAction(MainWindow)
        self.settingButton.setObjectName(u"settingButton")
        icon1 = QIcon()
        icon1.addFile(u":/menuBar/icons/settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settingButton.setIcon(icon1)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.message = QPlainTextEdit(self.centralwidget)
        self.message.setObjectName(u"message")
        self.message.setGeometry(QRect(4, 317, 361, 68))
        self.message.setStyleSheet(u"QPlainTextEdit {border: none;background: qlineargradient(spread:pad, angle:135, x1:0, y1:0, x2:1, y2:0, stop: 0 rgba(79,98,161,1), stop: 0.65 rgba(155,46,217,1));font-size:16px;font-family:\"Calibri\";}")
        self.direct = QPushButton(self.centralwidget)
        self.direct.setObjectName(u"direct")
        self.direct.setGeometry(QRect(370, 364, 35, 21))
        self.direct.setStyleSheet(u"QPushButton {background-color: rgb(212, 212, 212);;font-size: 13px;border: none;}QPushButton:hover {background-color: rgb(227, 227, 227);}")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/send.png", QSize(), QIcon.Normal, QIcon.Off)
        self.direct.setIcon(icon2)
        self.direct.setIconSize(QSize(33, 33))
        self.attachment = QPushButton(self.centralwidget)
        self.attachment.setObjectName(u"attachment")
        self.attachment.setGeometry(QRect(370, 317, 35, 21))
        self.attachment.setStyleSheet(u"QPushButton {background-color: rgb(212, 212, 212);;font-size: 13px;border: none;}QPushButton:hover {background-color: rgb(227, 227, 227);}")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/attachment.png", QSize(), QIcon.Normal, QIcon.Off)
        self.attachment.setIcon(icon3)
        self.attachment.setIconSize(QSize(24, 24))
        self.chat = QTextEdit(self.centralwidget)
        self.chat.setObjectName(u"chat")
        self.chat.setGeometry(QRect(4, 4, 401, 308))
        self.chat.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.chat.setStyleSheet(u"QTextEdit {border: none;background: rgb(245, 245, 245);font-size: 15px;font-family: \"Calibri\"}")
        self.chat.setTextInteractionFlags(Qt.NoTextInteraction)
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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SadGram", None))
        self.settingButton.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.message.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter your message", None))
        self.direct.setText("")
        self.attachment.setText("")
        self.chat.setPlaceholderText("")
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
    # retranslateUi

