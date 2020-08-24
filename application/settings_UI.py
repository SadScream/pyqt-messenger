# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(410, 140)
        Dialog.setMinimumSize(QSize(410, 140))
        Dialog.setMaximumSize(QSize(410, 140))
        icon = QIcon()
        icon.addFile(u"icons/settings.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.generalBox = QGroupBox(Dialog)
        self.generalBox.setObjectName(u"generalBox")
        self.generalBox.setGeometry(QRect(10, 10, 391, 81))
        self.generalBox.setStyleSheet(u"QGroupBox {\n"
"font-size: 12px;\n"
"}\n"
"QLabel {\n"
"font-size: 13px;\n"
"}")
        self.formLayoutWidget = QWidget(self.generalBox)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(9, 20, 201, 48))
        self.generalForm = QFormLayout(self.formLayoutWidget)
        self.generalForm.setObjectName(u"generalForm")
        self.generalForm.setContentsMargins(0, 0, 0, 0)
        self.nicknameLabel = QLabel(self.formLayoutWidget)
        self.nicknameLabel.setObjectName(u"nicknameLabel")
        self.nicknameLabel.setStyleSheet(u"")

        self.generalForm.setWidget(0, QFormLayout.LabelRole, self.nicknameLabel)

        self.nicknameLine = QLineEdit(self.formLayoutWidget)
        self.nicknameLine.setObjectName(u"nicknameLine")
        self.nicknameLine.setContextMenuPolicy(Qt.NoContextMenu)
        self.nicknameLine.setAcceptDrops(False)
        self.nicknameLine.setInputMethodHints(Qt.ImhLatinOnly)
        self.nicknameLine.setMaxLength(13)
        self.nicknameLine.setClearButtonEnabled(False)

        self.generalForm.setWidget(0, QFormLayout.FieldRole, self.nicknameLine)

        self.hostLabel = QLabel(self.formLayoutWidget)
        self.hostLabel.setObjectName(u"hostLabel")
        self.hostLabel.setStyleSheet(u"")

        self.generalForm.setWidget(1, QFormLayout.LabelRole, self.hostLabel)

        self.hostLine = QLineEdit(self.formLayoutWidget)
        self.hostLine.setObjectName(u"hostLine")
        self.hostLine.setAcceptDrops(False)
        self.hostLine.setInputMethodHints(Qt.ImhLatinOnly)
        self.hostLine.setMaxLength(16)

        self.generalForm.setWidget(1, QFormLayout.FieldRole, self.hostLine)

        self.loading_icon = QPushButton(self.generalBox)
        self.loading_icon.setObjectName(u"loading_icon")
        self.loading_icon.setGeometry(QRect(220, 13, 56, 56))
        self.loading_icon.setStyleSheet(u"QPushButton {\n"
"background-color: None;\n"
"border: none;\n"
"}\n"
"QPushButton:hover {\n"
"background-color: None;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/loading.png", QSize(), QIcon.Normal, QIcon.Off)
        self.loading_icon.setIcon(icon1)
        self.loading_icon.setIconSize(QSize(64, 64))
        self.horizontalLayoutWidget = QWidget(Dialog)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(240, 90, 158, 41))
        self.saveLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.saveLayout.setObjectName(u"saveLayout")
        self.saveLayout.setContentsMargins(0, 0, 0, 0)
        self.saveButton = QPushButton(self.horizontalLayoutWidget)
        self.saveButton.setObjectName(u"saveButton")

        self.saveLayout.addWidget(self.saveButton)

        self.cancelButton = QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setObjectName(u"cancelButton")

        self.saveLayout.addWidget(self.cancelButton)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Settings", None))
        self.generalBox.setTitle(QCoreApplication.translate("Dialog", u"General", None))
        self.nicknameLabel.setText(QCoreApplication.translate("Dialog", u"Nickname", None))
        self.nicknameLine.setPlaceholderText("")
        self.hostLabel.setText(QCoreApplication.translate("Dialog", u"Host", None))
        self.hostLine.setText("")
        self.loading_icon.setText("")
        self.saveButton.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.cancelButton.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

