# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'networkident_ui.ui'
#
# Created: Wed Feb 13 11:44:14 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NetworkIdent(object):
    def setupUi(self, NetworkIdent):
        NetworkIdent.setObjectName("NetworkIdent")
        NetworkIdent.resize(655, 445)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NetworkIdent.sizePolicy().hasHeightForWidth())
        NetworkIdent.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(NetworkIdent)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.networksTree = QtGui.QTreeWidget(NetworkIdent)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.networksTree.sizePolicy().hasHeightForWidth())
        self.networksTree.setSizePolicy(sizePolicy)
        self.networksTree.setObjectName("networksTree")
        self.horizontalLayout.addWidget(self.networksTree)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.networkLabel = QtGui.QLabel(NetworkIdent)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.networkLabel.sizePolicy().hasHeightForWidth())
        self.networkLabel.setSizePolicy(sizePolicy)
        self.networkLabel.setFrameShape(QtGui.QFrame.Panel)
        self.networkLabel.setFrameShadow(QtGui.QFrame.Raised)
        self.networkLabel.setText("")
        self.networkLabel.setObjectName("networkLabel")
        self.verticalLayout.addWidget(self.networkLabel)
        self.servicesTree = QtGui.QTreeWidget(NetworkIdent)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.servicesTree.sizePolicy().hasHeightForWidth())
        self.servicesTree.setSizePolicy(sizePolicy)
        self.servicesTree.setObjectName("servicesTree")
        self.verticalLayout.addWidget(self.servicesTree)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(NetworkIdent)
        QtCore.QMetaObject.connectSlotsByName(NetworkIdent)

    def retranslateUi(self, NetworkIdent):
        NetworkIdent.setWindowTitle(QtGui.QApplication.translate("NetworkIdent", "Network Identification", None, QtGui.QApplication.UnicodeUTF8))
        self.networksTree.headerItem().setText(0, QtGui.QApplication.translate("NetworkIdent", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.networksTree.headerItem().setText(1, QtGui.QApplication.translate("NetworkIdent", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.networksTree.headerItem().setText(2, QtGui.QApplication.translate("NetworkIdent", "Timestamp", None, QtGui.QApplication.UnicodeUTF8))
        self.servicesTree.headerItem().setText(0, QtGui.QApplication.translate("NetworkIdent", "Service", None, QtGui.QApplication.UnicodeUTF8))
        self.servicesTree.headerItem().setText(1, QtGui.QApplication.translate("NetworkIdent", "Value", None, QtGui.QApplication.UnicodeUTF8))

