# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'text_widget.ui'
#
# Created: Mon Jan 28 12:05:36 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_TextWidget(object):
    def setupUi(self, TextWidget):
        TextWidget.setObjectName("TextWidget")
        TextWidget.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(TextWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textContainer = QtGui.QTextEdit(TextWidget)
        self.textContainer.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textContainer.setReadOnly(True)
        self.textContainer.setObjectName("textContainer")
        self.horizontalLayout.addWidget(self.textContainer)

        self.retranslateUi(TextWidget)
        QtCore.QMetaObject.connectSlotsByName(TextWidget)

    def retranslateUi(self, TextWidget):
        TextWidget.setWindowTitle(QtGui.QApplication.translate("TextWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))

