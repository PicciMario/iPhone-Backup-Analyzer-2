# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'safaristate_ui.ui'
#
# Created: Wed Feb 13 11:44:14 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SafariState(object):
    def setupUi(self, SafariState):
        SafariState.setObjectName("SafariState")
        SafariState.resize(577, 417)
        self.verticalLayout = QtGui.QVBoxLayout(SafariState)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtGui.QLabel(SafariState)
        self.label_2.setFrameShape(QtGui.QFrame.Panel)
        self.label_2.setFrameShadow(QtGui.QFrame.Raised)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.documentsTree = QtGui.QTreeWidget(SafariState)
        self.documentsTree.setObjectName("documentsTree")
        self.verticalLayout.addWidget(self.documentsTree)
        self.label_3 = QtGui.QLabel(SafariState)
        self.label_3.setFrameShape(QtGui.QFrame.Panel)
        self.label_3.setFrameShadow(QtGui.QFrame.Raised)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.thumbLabel = QtGui.QLabel(SafariState)
        self.thumbLabel.setText("")
        self.thumbLabel.setObjectName("thumbLabel")
        self.horizontalLayout.addWidget(self.thumbLabel)
        self.listTree = QtGui.QTreeWidget(SafariState)
        self.listTree.setMouseTracking(False)
        self.listTree.setObjectName("listTree")
        self.listTree.headerItem().setText(0, "1")
        self.horizontalLayout.addWidget(self.listTree)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SafariState)
        QtCore.QMetaObject.connectSlotsByName(SafariState)

    def retranslateUi(self, SafariState):
        SafariState.setWindowTitle(QtGui.QApplication.translate("SafariState", "Safari State Explorer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SafariState", "Safari Open Tabs", None, QtGui.QApplication.UnicodeUTF8))
        self.documentsTree.headerItem().setText(0, QtGui.QApplication.translate("SafariState", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.documentsTree.headerItem().setText(1, QtGui.QApplication.translate("SafariState", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.documentsTree.headerItem().setText(2, QtGui.QApplication.translate("SafariState", "Timestamp", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SafariState", "Thumbnail and Back/Forward list for current tab (right click to copy/open)", None, QtGui.QApplication.UnicodeUTF8))

