# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'general_ui.ui'
#
# Created: Wed Feb 13 11:44:14 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_General(object):
    def setupUi(self, General):
        General.setObjectName("General")
        General.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(General)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.infoTree = QtGui.QTreeWidget(General)
        self.infoTree.setObjectName("infoTree")
        self.horizontalLayout.addWidget(self.infoTree)

        self.retranslateUi(General)
        QtCore.QMetaObject.connectSlotsByName(General)

    def retranslateUi(self, General):
        General.setWindowTitle(QtGui.QApplication.translate("General", "General Phone Info", None, QtGui.QApplication.UnicodeUTF8))
        self.infoTree.headerItem().setText(0, QtGui.QApplication.translate("General", "Key", None, QtGui.QApplication.UnicodeUTF8))
        self.infoTree.headerItem().setText(1, QtGui.QApplication.translate("General", "Value", None, QtGui.QApplication.UnicodeUTF8))

