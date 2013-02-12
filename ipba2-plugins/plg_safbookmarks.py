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
		
		if (daemon == False):
			self.populateUI()
			
	def insertBookmark(self, parent_node, parent_id):
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
			
			newNode = QtGui.QTreeWidgetItem(parent_node)
			#newNode.setText(0, str(id))
			newNode.setText(0, title)
			self.ui.bookmarksTree.addTopLevelItem(newNode)
			
			#newnode = bookmarkstree.insert(parent_node, 'end', text=title, values=(id))
		
			if (num_children != 0):
				self.insertBookmark(newNode, id)
			
			# type 0 for simple bookmarks, not 0 for folders
			if (bookmark['type'] == 0):
			
				keyNode = QtGui.QTreeWidgetItem(newNode)
				keyNode.setText(0, "URL: " + str(bookmark['url'].encode("utf-8")))
				self.ui.bookmarksTree.addTopLevelItem(keyNode)	

				keyNode = QtGui.QTreeWidgetItem(newNode)
				keyNode.setText(0, "Editable: " + str(bookmark['editable']))
				self.ui.bookmarksTree.addTopLevelItem(keyNode)

				keyNode = QtGui.QTreeWidgetItem(newNode)
				keyNode.setText(0, "Deletable: " + str(bookmark['deletable']))
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