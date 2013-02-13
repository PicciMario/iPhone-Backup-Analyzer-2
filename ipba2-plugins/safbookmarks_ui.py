# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'safbookmarks_ui.ui'
#
# Created: Wed Feb 13 11:44:13 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SafBookmarks(object):
    def setupUi(self, SafBookmarks):
        SafBookmarks.setObjectName("SafBookmarks")
        SafBookmarks.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(SafBookmarks)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bookmarksTree = QtGui.QTreeWidget(SafBookmarks)
        self.bookmarksTree.setObjectName("bookmarksTree")
        self.horizontalLayout.addWidget(self.bookmarksTree)

        self.retranslateUi(SafBookmarks)
        QtCore.QMetaObject.connectSlotsByName(SafBookmarks)

    def retranslateUi(self, SafBookmarks):
        SafBookmarks.setWindowTitle(QtGui.QApplication.translate("SafBookmarks", "Safari Bookmarks", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmarksTree.headerItem().setText(0, QtGui.QApplication.translate("SafBookmarks", "Bookmarks", None, QtGui.QApplication.UnicodeUTF8))

