# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prova_ui.ui'
#
# Created: Mon Jan 28 12:09:37 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Prova(object):
    def setupUi(self, Prova):
        Prova.setObjectName("Prova")
        Prova.resize(400, 300)

        self.retranslateUi(Prova)
        QtCore.QMetaObject.connectSlotsByName(Prova)

    def retranslateUi(self, Prova):
        Prova.setWindowTitle(QtGui.QApplication.translate("Prova", "Form", None, QtGui.QApplication.UnicodeUTF8))

