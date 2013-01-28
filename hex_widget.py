# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hex_widget.ui'
#
# Created: Mon Jan 28 12:05:36 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_HexWidget(object):
    def setupUi(self, HexWidget):
        HexWidget.setObjectName("HexWidget")
        HexWidget.resize(380, 440)
        self.verticalLayout = QtGui.QVBoxLayout(HexWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.buttonLeft = QtGui.QPushButton(HexWidget)
        self.buttonLeft.setObjectName("buttonLeft")
        self.gridLayout.addWidget(self.buttonLeft, 0, 2, 1, 1)
        self.buttonRight = QtGui.QPushButton(HexWidget)
        self.buttonRight.setObjectName("buttonRight")
        self.gridLayout.addWidget(self.buttonRight, 0, 3, 1, 1)
        self.buttonTop = QtGui.QPushButton(HexWidget)
        self.buttonTop.setObjectName("buttonTop")
        self.gridLayout.addWidget(self.buttonTop, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.hexTable = QtGui.QTableWidget(HexWidget)
        self.hexTable.setRowCount(10)
        self.hexTable.setColumnCount(17)
        self.hexTable.setObjectName("hexTable")
        self.hexTable.setColumnCount(17)
        self.hexTable.setRowCount(10)
        self.verticalLayout.addWidget(self.hexTable)

        self.retranslateUi(HexWidget)
        QtCore.QMetaObject.connectSlotsByName(HexWidget)

    def retranslateUi(self, HexWidget):
        HexWidget.setWindowTitle(QtGui.QApplication.translate("HexWidget", "Hex Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonLeft.setText(QtGui.QApplication.translate("HexWidget", "<", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRight.setText(QtGui.QApplication.translate("HexWidget", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonTop.setText(QtGui.QApplication.translate("HexWidget", "<<", None, QtGui.QApplication.UnicodeUTF8))

