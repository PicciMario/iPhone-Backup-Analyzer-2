from PySide import QtCore, QtGui
from note_ui import Ui_Note

import os, sqlite3, sys
from datetime import datetime
from string import *

PLUGIN_NAME = "Note Browser"
import plugins_utils

# retrieve modules from ipba root directory
import plistutils

class NoteWidget(QtGui.QWidget):
	
	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_Note()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		self.filename = os.path.join(self.backup_path, plugins_utils.realFileName(cursor, filename="notes.sqlite", domaintype="HomeDomain"))

		# check if files exist
		if (not os.path.isfile(self.filename)):
			raise Exception("Note database not found: \"%s\""%self.filename)
			
		if (daemon == False):
			self.populateUI()


	def populateUI(self):
	
		QtCore.QObject.connect(self.ui.noteTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onNoteClick)
		
		self.ui.noteTree.setColumnHidden(0,True)
	
		# opening database
		tempdb = sqlite3.connect(self.filename)
		tempdb.row_factory = sqlite3.Row
		tempcur = tempdb.cursor() 

		query = 'SELECT Z_PK, ZTITLE FROM znote;'
		tempcur.execute(query)
		notes = tempcur.fetchall()
		
		for note in notes:
			
			id = note['Z_PK']
			title = note['ZTITLE']
			if (len(title) > 25):
				title = "%s..."%title[:25]
			
			noteNode = QtGui.QTreeWidgetItem(None)
			noteNode.setText(0, str(id))
			noteNode.setText(1, title)
			self.ui.noteTree.addTopLevelItem(noteNode)			

		# closing database
		tempdb.close()
	

	def onNoteClick(self):
	
		self.ui.noteText.clear()
		self.ui.text_author.clear()	
		self.ui.text_summary.clear()	
		self.ui.text_created.clear()	
		self.ui.text_modified.clear()
		
		currentSelectedElement = self.ui.noteTree.currentItem()
		if (currentSelectedElement): pass
		else: return
		
		# opening database
		tempdb = sqlite3.connect(self.filename)
		tempdb.row_factory = sqlite3.Row
		tempcur = tempdb.cursor() 
		
		noteID = currentSelectedElement.text(0)
		
		# retrieve more info from ZNOTE
		query = 'SELECT ZAUTHOR, ZSUMMARY, ZCREATIONDATE, ZMODIFICATIONDATE FROM znote WHERE Z_PK = ?;'
		tempcur.execute(query, (noteID,))
		content = tempcur.fetchall()
		
		if (len(content) == 0):
			tempdb.close()
			return
		else:
			content = content[0]
		
		creDateUnix = content['ZCREATIONDATE'] + 978307200 #JAN 1 1970
		creDate = datetime.fromtimestamp(creDateUnix).strftime('%Y-%m-%d %H:%M:%S')

		modDateUnix = content['ZMODIFICATIONDATE'] + 978307200 #JAN 1 1970
		modDate = datetime.fromtimestamp(modDateUnix).strftime('%Y-%m-%d %H:%M:%S')
		
		self.ui.text_author.setText(content['ZAUTHOR'])		
		self.ui.text_summary.setText(content['ZSUMMARY'])		
		self.ui.text_created.setText(creDate)		
		self.ui.text_modified.setText(modDate)		
		
		# retrieve content from ZNOTEBODY
		query = 'SELECT ZCONTENT FROM znotebody WHERE ZOWNER = ?;'
		tempcur.execute(query, (noteID,))
		content = tempcur.fetchall()
		
		if (len(content) == 0):
			tempdb.close()
			return
		else:
			content = content[0]
		
		self.ui.noteText.setText(content['ZCONTENT'])

		# closing database
		tempdb.close()
	
def main(cursor, path):
	return NoteWidget(cursor, path)