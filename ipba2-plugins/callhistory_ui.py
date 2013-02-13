# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'callhistory_ui.ui'
#
# Created: Wed Feb 13 11:44:13 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_CallHistory(object):
    def setupUi(self, CallHistory):
        CallHistory.setObjectName("CallHistory")
        CallHistory.resize(629, 470)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(CallHistory)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.toolBox = QtGui.QToolBox(CallHistory)
        self.toolBox.setObjectName("toolBox")
        self.page = QtGui.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 611, 398))
        self.page.setObjectName("page")
        self.horizontalLayout = QtGui.QHBoxLayout(self.page)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.callsTable = QtGui.QTableWidget(self.page)
        self.callsTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.callsTable.setObjectName("callsTable")
        self.callsTable.setColumnCount(6)
        self.callsTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.callsTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.callsTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.callsTable.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.callsTable.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.callsTable.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.callsTable.setHorizontalHeaderItem(5, item)
        self.horizontalLayout.addWidget(self.callsTable)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 98, 89))
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.page_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.keysTable = QtGui.QTableWidget(self.page_2)
        self.keysTable.setObjectName("keysTable")
        self.keysTable.setColumnCount(2)
        self.keysTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.keysTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.keysTable.setHorizontalHeaderItem(1, item)
        self.horizontalLayout_2.addWidget(self.keysTable)
        self.toolBox.addItem(self.page_2, "")
        self.horizontalLayout_3.addWidget(self.toolBox)

        self.retranslateUi(CallHistory)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CallHistory)

    def retranslateUi(self, CallHistory):
        CallHistory.setWindowTitle(QtGui.QApplication.translate("CallHistory", "Call History", None, QtGui.QApplication.UnicodeUTF8))
        self.callsTable.setSortingEnabled(True)
        self.callsTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("CallHistory", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.callsTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("CallHistory", "Address", None, QtGui.QApplication.UnicodeUTF8))
        self.callsTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("CallHistory", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.callsTable.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("CallHistory", "Duration", None, QtGui.QApplication.UnicodeUTF8))
        self.callsTable.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("CallHistory", "Flags", None, QtGui.QApplication.UnicodeUTF8))
        self.callsTable.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("CallHistory", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QtGui.QApplication.translate("CallHistory", "Calls list", None, QtGui.QApplication.UnicodeUTF8))
        self.keysTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("CallHistory", "Key", None, QtGui.QApplication.UnicodeUTF8))
        self.keysTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("CallHistory", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QtGui.QApplication.translate("CallHistory", "Calls data", None, QtGui.QApplication.UnicodeUTF8))

