from PySide import QtCore, QtGui
from safaristate_ui import Ui_SafariState

import os, sqlite3
from datetime import datetime

PLUGIN_NAME = "Safari State"
import plugins_utils

# retrieve modules from ipba root directory
import plistutils

class SafariStateWidget(QtGui.QWidget):
	
	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_SafariState()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		self.filename = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename="SuspendState.plist", domaintype="HomeDomain"))

		if (not os.path.isfile(self.filename)):
			raise Exception("Safari State file not found: \"%s\""%self.filename)
		
		QtCore.QObject.connect(self.ui.documentsTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onTreeClick)
		
		self.ui.listTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		QtCore.QObject.connect(self.ui.listTree, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenu)
		
		self.ui.documentsTree.setColumnHidden(0,True)
		self.ui.documentsTree.setColumnWidth(1,150)

		if (daemon == False):
			self.populateUI()


	def populateUI(self):
		
		documents = plistutils.readPlist(self.filename)['SafariStateDocuments']
		
		index = 0
		for document in documents:
		
			documentTitle = document['SafariStateDocumentTitle']
			documentTimestamp = document['SafariStateDocumentLastViewedTime'] + 978307200 #JAN 1 1970
			documentTimestamp = datetime.fromtimestamp(documentTimestamp).strftime('%Y-%m-%d %H:%M:%S')
			
			newElement = QtGui.QTreeWidgetItem(None)
			newElement.setText(0, str(index))
			newElement.setText(1, documentTimestamp)
			newElement.setText(2, documentTitle)
			self.ui.documentsTree.addTopLevelItem(newElement)
			
			index += 1


	def ctxMenu(self, pos):
	
		currentSelectedElement = self.ui.listTree.currentItem()
		if (currentSelectedElement): pass
		else: return
		
		menu =  QtGui.QMenu();
		action1 = QtGui.QAction("Copy", self)
		action1.triggered.connect(self.copySelected)
		menu.addAction(action1)			
	
		# if url (QTreeWidgetItem with a parent)
		if (currentSelectedElement.parent()):
			action1 = QtGui.QAction("Open in browser", self)
			action1.triggered.connect(self.openSelectedURL)
			menu.addAction(action1)
			
		menu.exec_(self.ui.listTree.mapToGlobal(pos));
	
	def copySelected(self):
	
		currentSelectedElement = self.ui.listTree.currentItem()
		if (currentSelectedElement): pass
		else: return
	
		url = currentSelectedElement.text(0)
		
		clipboard = QtGui.QApplication.clipboard()
		clipboard.setText(url)

	def openSelectedURL(self):
	
		currentSelectedElement = self.ui.listTree.currentItem()
		if (currentSelectedElement): pass
		else: return
	
		url = currentSelectedElement.text(0)
		
		QtGui.QDesktopServices.openUrl(url)
		
	def onTreeClick(self):
		
		# retrieving selected network
		currentSelectedElement = self.ui.documentsTree.currentItem()
		if (currentSelectedElement): pass
		else: return
		
		documents = plistutils.readPlist(self.filename)['SafariStateDocuments']
		
		currentTabIndex = int(currentSelectedElement.text(0))
		currentTab = documents[currentTabIndex]
		currentList = currentTab['SafariStateDocumentBackForwardList']
		
		currentOpenElement = currentTab['SafariStateDocumentBackForwardList']['current']
		
		self.ui.listTree.clear()
		
		index = 0
		for element in currentList['entries']:
		
			try:
				title = element['title']
			except:
				title = "<non title>"

			titleElement = QtGui.QTreeWidgetItem(None)
			titleElement.setText(0, title)
			self.ui.listTree.addTopLevelItem(titleElement)

			urlElement = QtGui.QTreeWidgetItem(titleElement)
			urlElement.setText(0, element[''])			
			self.ui.listTree.addTopLevelItem(urlElement)
			
			if (index == currentOpenElement):
				titleElement.setBackground(0, QtCore.Qt.yellow)		
			
			index = index + 1
		
		# look for page appearance cache
		cacheFileName = "%s.png"%currentTab['SafariStateDocumentUUID']
		cacheFile = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename=cacheFileName, domaintype="HomeDomain"))
		if (os.path.isfile(cacheFile)):
			pic = QtGui.QPixmap(cacheFile).scaled(200, 200, QtCore.Qt.KeepAspectRatio)	
			self.ui.thumbLabel.setPixmap(pic) 
			self.ui.thumbLabel.show() 
		else:
			self.ui.thumbLabel.hide()
	
def main(cursor, path):
	return SafariStateWidget(cursor, path)