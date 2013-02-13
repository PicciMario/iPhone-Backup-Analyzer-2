# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addressbook_ui.ui'
#
# Created: Wed Feb 13 11:44:14 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_AddressBook(object):
    def setupUi(self, AddressBook):
        AddressBook.setObjectName("AddressBook")
        AddressBook.resize(664, 460)
        self.horizontalLayout = QtGui.QHBoxLayout(AddressBook)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.contactsTree = QtGui.QTreeWidget(AddressBook)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contactsTree.sizePolicy().hasHeightForWidth())
        self.contactsTree.setSizePolicy(sizePolicy)
        self.contactsTree.setObjectName("contactsTree")
        self.horizontalLayout.addWidget(self.contactsTree)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.contactsTable = QtGui.QTableWidget(AddressBook)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contactsTable.sizePolicy().hasHeightForWidth())
        self.contactsTable.setSizePolicy(sizePolicy)
        self.contactsTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.contactsTable.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.contactsTable.setRowCount(0)
        self.contactsTable.setColumnCount(2)
        self.contactsTable.setObjectName("contactsTable")
        self.contactsTable.setColumnCount(2)
        self.contactsTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.contactsTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.contactsTable.setHorizontalHeaderItem(1, item)
        self.contactsTable.horizontalHeader().setStretchLastSection(True)
        self.contactsTable.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.contactsTable)
        self.imageLabel = QtGui.QLabel(AddressBook)
        self.imageLabel.setFrameShape(QtGui.QFrame.Box)
        self.imageLabel.setFrameShadow(QtGui.QFrame.Raised)
        self.imageLabel.setText("")
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setMargin(1)
        self.imageLabel.setObjectName("imageLabel")
        self.verticalLayout.addWidget(self.imageLabel)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(AddressBook)
        QtCore.QMetaObject.connectSlotsByName(AddressBook)

    def retranslateUi(self, AddressBook):
        AddressBook.setWindowTitle(QtGui.QApplication.translate("AddressBook", "Address Book Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.contactsTree.headerItem().setText(0, QtGui.QApplication.translate("AddressBook", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.contactsTree.headerItem().setText(1, QtGui.QApplication.translate("AddressBook", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.contactsTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("AddressBook", "Key", None, QtGui.QApplication.UnicodeUTF8))
        self.contactsTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("AddressBook", "Value", None, QtGui.QApplication.UnicodeUTF8))

