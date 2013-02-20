from PySide import QtCore, QtGui
from safbookmarks_ui import Ui_SafBookmarks

import os, sqlite3
from datetime import datetime

PLUGIN_NAME = "Safari Bookmarks"
import plugins_utils

class SafBookmarksWidget(QtGui.QWidget):
	
	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_SafBookmarks()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		self.filename = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename="Bookmarks.db", domaintype="HomeDomain"))

		if (not os.path.isfile(self.filename)):
			raise Exception("Safari Bookmarks Database not found: \"%s\""%self.filename)
	
		self.ui.bookmarksTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		QtCore.QObject.connect(self.ui.bookmarksTree, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenu)
	
		if (daemon == False):
			self.populateUI()


	def ctxMenu(self, pos):
	
		currentSelectedElement = self.ui.bookmarksTree.currentItem()
		if (currentSelectedElement): pass
		else: return
		
		# if url
		if (len(currentSelectedElement.text(1)) > 0):
			
			menu =  QtGui.QMenu();
			
			action1 = QtGui.QAction("Open in browser", self)
			action1.triggered.connect(self.openSelectedURL)
			menu.addAction(action1)

			action1 = QtGui.QAction("Copy URL", self)
			action1.triggered.connect(self.copySelected)
			menu.addAction(action1)
			
			menu.exec_(self.ui.bookmarksTree.mapToGlobal(pos));		

	def openSelectedURL(self):
	
		currentSelectedElement = self.ui.bookmarksTree.currentItem()
		if (currentSelectedElement): pass
		else: return
	
		url = currentSelectedElement.text(1)
		
		QtGui.QDesktopServices.openUrl(url)
		
	def copySelected(self):
	
		currentSelectedElement = self.ui.bookmarksTree.currentItem()
		if (currentSelectedElement): pass
		else: return
	
		url = currentSelectedElement.text(1)
		
		clipboard = QtGui.QApplication.clipboard()
		clipboard.setText(url)

			
	def insertBookmark(self, parent_node, parent_id):
		query = "SELECT id, title, num_children, type, url, editable, deletable, order_index, external_uuid FROM bookmarks WHERE parent = \"%s\" ORDER BY order_index"%parent_id
		self.tempcur.execute(query)
		bookmarks = self.tempcur.fetchall()
		
		folderIcon = self.style().standardIcon(QtGui.QStyle.SP_DirIcon) 
		urlIcon = self.style().standardIcon(QtGui.QStyle.SP_FileDialogContentsView) 
		
		for bookmark in bookmarks:
			id = bookmark['id']
			title = bookmark['title']
			num_children = bookmark['num_children']
			
			# creating new node
			newNode = QtGui.QTreeWidgetItem(parent_node)
			
			# setting title
			#title = str(title.encode("utf-8"))
			if (bookmark['type'] != 0):
				title += " (%i)"%num_children
				newNode.setIcon(0, folderIcon) 
			else:
				newNode.setIcon(0, urlIcon)
			
			newNode.setText(0, title)
			
			# adding node to bookmarks tree
			self.ui.bookmarksTree.addTopLevelItem(newNode)
		
			if (num_children != 0):
				self.insertBookmark(newNode, id)
			
			# type 0 for simple bookmarks, not 0 for folders
			if (bookmark['type'] == 0):
			
				newNode.setText(1, bookmark['url'])
			
				keyNode = QtGui.QTreeWidgetItem(newNode)
				keyNode.setText(0, bookmark['url'])
				keyNode.setText(1, bookmark['url'])
				self.ui.bookmarksTree.addTopLevelItem(keyNode)	


	def printBookmark(self, parent_id):
	
		ritorno = ""
	
		# opening database
		self.tempdb = sqlite3.connect(self.filename)
		self.tempdb.row_factory = sqlite3.Row
		self.tempcur = self.tempdb.cursor()
	
		query = "SELECT id, title, num_children, type, url, editable, deletable, order_index, external_uuid FROM bookmarks WHERE parent = \"%s\" ORDER BY order_index"%parent_id
		self.tempcur.execute(query)
		bookmarks = self.tempcur.fetchall()
		for bookmark in bookmarks:
			id = bookmark['id']
			title = bookmark['title']
			num_children = bookmark['num_children']
			
			title = str(title.encode("utf-8"))
			if (bookmark['type'] != 0):
				title = "[" + title + "] (%i)"%num_children
			else:
				ref = "<a href=\"%s\">"%str(bookmark['url'].encode("utf-8"))
				title = ref + title + "</a>"

			
			ritorno += "<ul>"

			ritorno += "<li>"
			ritorno += title			
		
			if (num_children != 0):
				#ritorno += "<li>"
				ritorno += self.printBookmark(id)
			
			ritorno += "</ul>"

		# closing database
		self.tempdb.close()	

		return ritorno
	
	def populateUI(self):

		# opening database
		self.tempdb = sqlite3.connect(self.filename)
		self.tempdb.row_factory = sqlite3.Row
		self.tempcur = self.tempdb.cursor()
	
		# populating tree with Safari Bookmarks
		self.insertBookmark(None, 0)

		# closing database
		self.tempdb.close()

def main(cursor, path):
	return SafBookmarksWidget(cursor, path)

def report(cursor, path):
	safBookManager = SafBookmarksWidget(cursor, path, False)
	ritorno = "<h1>Safari Bookmarks</h1>"
	ritorno += safBookManager.printBookmark(0)
	del safBookManager
	return (ritorno, None)