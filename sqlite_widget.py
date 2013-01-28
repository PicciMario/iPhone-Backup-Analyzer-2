# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sqlite_widget.ui'
#
# Created: Mon Jan 28 12:05:36 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SqliteWidget(object):
    def setupUi(self, SqliteWidget):
        SqliteWidget.setObjectName("SqliteWidget")
        SqliteWidget.resize(619, 361)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(SqliteWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tablesList = QtGui.QTreeWidget(SqliteWidget)
        self.tablesList.setMaximumSize(QtCore.QSize(210, 16777215))
        self.tablesList.setIndentation(0)
        self.tablesList.setObjectName("tablesList")
        self.horizontalLayout_2.addWidget(self.tablesList)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonLeft = QtGui.QPushButton(SqliteWidget)
        self.buttonLeft.setMaximumSize(QtCore.QSize(40, 16777215))
        self.buttonLeft.setObjectName("buttonLeft")
        self.horizontalLayout.addWidget(self.buttonLeft)
        self.recordLabel = QtGui.QLabel(SqliteWidget)
        self.recordLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.recordLabel.setText("")
        self.recordLabel.setObjectName("recordLabel")
        self.horizontalLayout.addWidget(self.recordLabel)
        self.buttonRight = QtGui.QPushButton(SqliteWidget)
        self.buttonRight.setMinimumSize(QtCore.QSize(0, 0))
        self.buttonRight.setMaximumSize(QtCore.QSize(40, 16777215))
        self.buttonRight.setObjectName("buttonRight")
        self.horizontalLayout.addWidget(self.buttonRight)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableContent = QtGui.QTableWidget(SqliteWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableContent.sizePolicy().hasHeightForWidth())
        self.tableContent.setSizePolicy(sizePolicy)
        self.tableContent.setObjectName("tableContent")
        self.tableContent.setColumnCount(0)
        self.tableContent.setRowCount(0)
        self.verticalLayout.addWidget(self.tableContent)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(SqliteWidget)
        QtCore.QMetaObject.connectSlotsByName(SqliteWidget)

    def retranslateUi(self, SqliteWidget):
        SqliteWidget.setWindowTitle(QtGui.QApplication.translate("SqliteWidget", "SQLite Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.tablesList.headerItem().setText(0, QtGui.QApplication.translate("SqliteWidget", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.tablesList.headerItem().setText(1, QtGui.QApplication.translate("SqliteWidget", "#", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonLeft.setText(QtGui.QApplication.translate("SqliteWidget", "<<", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRight.setText(QtGui.QApplication.translate("SqliteWidget", ">>", None, QtGui.QApplication.UnicodeUTF8))

