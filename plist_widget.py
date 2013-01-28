# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plist_widget.ui'
#
# Created: Mon Jan 28 12:05:37 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PlistWidget(object):
    def setupUi(self, PlistWidget):
        PlistWidget.setObjectName("PlistWidget")
        PlistWidget.resize(457, 347)
        self.horizontalLayout = QtGui.QHBoxLayout(PlistWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plistTree = QtGui.QTreeWidget(PlistWidget)
        self.plistTree.setObjectName("plistTree")
        self.horizontalLayout.addWidget(self.plistTree)

        self.retranslateUi(PlistWidget)
        QtCore.QMetaObject.connectSlotsByName(PlistWidget)

    def retranslateUi(self, PlistWidget):
        PlistWidget.setWindowTitle(QtGui.QApplication.translate("PlistWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.plistTree.headerItem().setText(0, QtGui.QApplication.translate("PlistWidget", "Data", None, QtGui.QApplication.UnicodeUTF8))

