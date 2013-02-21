from PySide import QtCore, QtGui
from safarihistory_ui import Ui_SafariHistory

import os, sqlite3, plistlib
from datetime import datetime

PLUGIN_NAME = "Safari History"
import plugins_utils

# retrieve modules from ipba root directory
import plistutils

class SafariHistoryWidget(QtGui.QWidget):
	
	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_SafariHistory()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		self.filename = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename="History.plist", domaintype="HomeDomain", path="Library/Safari"))

		if (not os.path.isfile(self.filename)):
			raise Exception("Safari history file not found: \"%s\""%self.filename)
		
		self.ui.historyTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		QtCore.QObject.connect(self.ui.historyTree, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenu)
		
		if (daemon == False):
		
			self.ui.historyTree.setColumnHidden(0,True)
			self.ui.historyTree.setColumnWidth(1,150)
			QtCore.QObject.connect(self.ui.historyTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onTreeClick)
			
			self.populateUI()


	def populateUI(self):
	
		self.historyRecords = plistutils.readPlist(self.filename)['WebHistoryDates']
		
		index = 0
		for record in self.historyRecords:

			element = QtGui.QTreeWidgetItem(None)
			element.setText(0, str(index))			
			
			if ('lastVisitedDate' in record.keys()):
				dateUnix = float(record['lastVisitedDate']) + 978307200 #JAN 1 1970
				dateStr = datetime.fromtimestamp(dateUnix).strftime('%Y-%m-%d %H:%M:%S')
				element.setText(1, dateStr)	
			
			if ('title' in record.keys()):
				title = record['title']
			else:
				title = record['']
			element.setText(2, title)
			
			# url saved in hidden column for context menu
			element.setText(3, record[''])
			
			self.ui.historyTree.addTopLevelItem(element)
			
			index += 1			


	def ctxMenu(self, pos):
	
		currentSelectedElement = self.ui.historyTree.currentItem()
		if (currentSelectedElement): pass
		else: return

		menu =  QtGui.QMenu();
		
		action1 = QtGui.QAction("Open in browser", self)
		action1.triggered.connect(self.openSelectedURL)
		menu.addAction(action1)

		action1 = QtGui.QAction("Copy URL", self)
		action1.triggered.connect(self.copySelected)
		menu.addAction(action1)
		
		menu.exec_(self.ui.historyTree.mapToGlobal(pos));			

	def openSelectedURL(self):
	
		currentSelectedElement = self.ui.historyTree.currentItem()
		if (currentSelectedElement): pass
		else: return
	
		url = currentSelectedElement.text(3)
		
		QtGui.QDesktopServices.openUrl(url)
		
	def copySelected(self):
	
		currentSelectedElement = self.ui.historyTree.currentItem()
		if (currentSelectedElement): pass
		else: return
	
		url = currentSelectedElement.text(3)
		
		clipboard = QtGui.QApplication.clipboard()
		clipboard.setText(url)
		

	def onTreeClick(self):
		
		# retrieving selected network
		currentSelectedElement = self.ui.historyTree.currentItem()
		if (currentSelectedElement): pass
		else: return

		currentSelectedID = int(currentSelectedElement.text(0))
		
		currentHistory = self.historyRecords[currentSelectedID]
		
		self.ui.label_title.clear()
		self.ui.label_url.clear()
		self.ui.label_redirurl.clear()
		self.ui.label_visitcount.clear()
		
		self.ui.label_url.setText(currentHistory[''])
		if ("title" in currentHistory.keys()):
			self.ui.label_title.setText(currentHistory['title'])		
		if ("visitCount" in currentHistory.keys()):
			self.ui.label_visitcount.setText(str(currentHistory['visitCount']))	
		if ("redirectURLs" in currentHistory.keys()):
			for element in currentHistory['redirectURLs']:
				self.ui.label_redirurl.append(element)	
		
def main(cursor, path):
	return SafariHistoryWidget(cursor, path)		