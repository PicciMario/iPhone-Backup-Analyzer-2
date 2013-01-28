# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'image_widget.ui'
#
# Created: Mon Jan 28 12:05:36 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ImageWidget(object):
    def setupUi(self, ImageWidget):
        ImageWidget.setObjectName("ImageWidget")
        ImageWidget.resize(418, 368)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ImageWidget.sizePolicy().hasHeightForWidth())
        ImageWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(ImageWidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.toolBox = QtGui.QToolBox(ImageWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBox.setBaseSize(QtCore.QSize(0, 0))
        self.toolBox.setObjectName("toolBox")
        self.page1 = QtGui.QWidget()
        self.page1.setGeometry(QtCore.QRect(0, 0, 400, 296))
        self.page1.setObjectName("page1")
        self.horizontalLayout = QtGui.QHBoxLayout(self.page1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.imageLabel = QtGui.QLabel(self.page1)
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")
        self.horizontalLayout.addWidget(self.imageLabel)
        self.toolBox.addItem(self.page1, "")
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 400, 296))
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.page_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.exifTable = QtGui.QTableWidget(self.page_2)
        self.exifTable.setAlternatingRowColors(True)
        self.exifTable.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.exifTable.setRowCount(0)
        self.exifTable.setColumnCount(3)
        self.exifTable.setObjectName("exifTable")
        self.exifTable.setColumnCount(3)
        self.exifTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.exifTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.exifTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.exifTable.setHorizontalHeaderItem(2, item)
        self.horizontalLayout_2.addWidget(self.exifTable)
        self.toolBox.addItem(self.page_2, "")
        self.horizontalLayout_3.addWidget(self.toolBox)

        self.retranslateUi(ImageWidget)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ImageWidget)

    def retranslateUi(self, ImageWidget):
        ImageWidget.setWindowTitle(QtGui.QApplication.translate("ImageWidget", "Image Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page1), QtGui.QApplication.translate("ImageWidget", "Image Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.exifTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("ImageWidget", "Tag", None, QtGui.QApplication.UnicodeUTF8))
        self.exifTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("ImageWidget", "Descr", None, QtGui.QApplication.UnicodeUTF8))
        self.exifTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("ImageWidget", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QtGui.QApplication.translate("ImageWidget", "EXIF data", None, QtGui.QApplication.UnicodeUTF8))

