from PySide import QtCore, QtGui
from sms_ui import Ui_SMS

import os, sqlite3, sys
from datetime import datetime
from string import *

PLUGIN_NAME = "SMS/iMessage Browser"
import plugins_utils

# retrieve modules from ipba root directory
import plistutils

class SMSWidget(QtGui.QWidget):
	
	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_SMS()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		self.cursor = cursor
		
		self.filename = os.path.join(self.backup_path, plugins_utils.realFileName(cursor, filename="sms.db", domaintype="HomeDomain"))

		# check if files exist
		if (not os.path.isfile(self.filename)):
			raise Exception("Messages database not found: \"%s\""%self.filename)
			
		if (daemon == False):
			self.populateUI()
			
			QtCore.QObject.connect(self.ui.threadsTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onTreeClick)
			self.ui.threadsTree.setColumnHidden(0,True)
			
			# attach context menu to rightclick on message attachment
			self.ui.messageTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			self.connect(self.ui.messageTable, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenu)				

	def populateUI(self):

		# opening database
		tempdb = sqlite3.connect(self.filename)
		tempdb.row_factory = sqlite3.Row
		tempcur = tempdb.cursor() 

		# populating tree with SMS groups
		query = "SELECT ROWID, chat_identifier FROM chat;"
		tempcur.execute(query)
		groups = tempcur.fetchall()
		
		for group in groups:
			groupid = group['ROWID']
			address = group['chat_identifier'].replace(' ', '')

			newElement = QtGui.QTreeWidgetItem(None)
			newElement.setText(0, str(groupid))
			newElement.setText(1, address)
			self.ui.threadsTree.addTopLevelItem(newElement)			

		# closing database
		tempdb.close()


	def ctxMenu(self, pos):	
		
		cell = self.ui.messageTable.itemAt(pos)
		self.link = cell.data(QtCore.Qt.UserRole) 
		
		if (self.link != None):
		
			menu =  QtGui.QMenu()
		
			action1 = QtGui.QAction("Open in standard viewer", self)
			action1.triggered.connect(self.openWithViewer)
			menu.addAction(action1)
		
			menu.exec_(self.ui.messageTable.mapToGlobal(pos));
	
	def openWithViewer(self):

		if sys.platform.startswith('linux'):
			subprocess.call(["xdg-open", self.link])
		else:
			os.startfile(self.link)

	def onTreeClick(self):
		
		# retrieving selected network
		currentSelectedElement = self.ui.threadsTree.currentItem()
		if (currentSelectedElement): pass
		else: return
		
		currentChat = int(currentSelectedElement.text(0))
		
		self.ui.threadLabel.setText(currentSelectedElement.text(1))

		# opening database
		tempdb = sqlite3.connect(self.filename)
		tempdb.row_factory = sqlite3.Row
		tempcur = tempdb.cursor()

		query = 'SELECT ROWID, text, date, is_from_me, cache_has_attachments FROM message INNER JOIN chat_message_join ON message.ROWID = chat_message_join.message_id WHERE chat_id = ?;'
		tempcur.execute(query, (currentChat,))
		messages = tempcur.fetchall()
		
		self.ui.messageTable.clear()
		
		# prepare table with enough rows
		# each message is a row, but each attachment also counts as one
		# so, we make an educated guess
		maxRows = len(messages) * 2
		if (maxRows < 100):
			maxRows += 100
		
		self.ui.messageTable.setRowCount(maxRows)
		self.ui.messageTable.setColumnCount(2)
		self.ui.messageTable.setHorizontalHeaderLabels(["Date", "Text"])
		
		row = 0
		for message in messages:
			
			documentTimestamp = message['date'] + 978307200 #JAN 1 1970
			documentTimestamp = datetime.fromtimestamp(documentTimestamp).strftime('%Y-%m-%d %H:%M:%S')
			if (message['is_from_me'] == 1):
				documentTimestamp = "Sent on:\n" + documentTimestamp
			else:
				documentTimestamp = "Received on:\n" + documentTimestamp
			newItem = QtGui.QTableWidgetItem(documentTimestamp)		
			self.ui.messageTable.setItem(row, 0, newItem)
			
			newItem = QtGui.QTableWidgetItem(message['text'])
			if (message['is_from_me'] == 1):
				newItem.setBackground(QtCore.Qt.green)
			else:
				newItem.setBackground(QtCore.Qt.gray)
			self.ui.messageTable.setItem(row, 1, newItem)
			
			row += 1
			
			if (message['cache_has_attachments'] == 1):
				query = 'SELECT ROWID, filename, mime_type FROM attachment INNER JOIN message_attachment_join ON message_attachment_join.attachment_id = attachment.ROWID WHERE message_attachment_join.message_id = ?;'
				tempcur.execute(query, (message['ROWID'], ))
				
				for attachment in tempcur.fetchall():
				
					attachmentFileName = attachment['filename']
					attachmentType = attachment['mime_type']
					
					attachmentPath = "/".join(os.path.dirname(attachmentFileName).split("/")[3:])
					attachmentName = os.path.basename(attachmentFileName)
					
					attachmentRealFilename = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename=attachmentName, path=attachmentPath, domaintype="MediaDomain"))
					
					if (not os.path.isfile(attachmentRealFilename)):
						newItem = QtGui.QTableWidgetItem("Attached file %s (id: %i) not found."%(attachmentFileName, attachment['ROWID']))
					
					else:
						
						if (attachmentType.split("/")[0] == "image"):
							newItem = QtGui.QTableWidgetItem(str(attachment['ROWID']))
							icon = QtGui.QIcon(attachmentRealFilename)
							newItem.setIcon(icon)		
							
						else:
							newItem = QtGui.QTableWidgetItem("Attached file %s (id: %i)."%(attachmentFileName, attachment['ROWID']))
					
						newItem.setData(QtCore.Qt.UserRole, attachmentRealFilename)
					
					if (message['is_from_me'] == 1):
						newItem.setBackground(QtCore.Qt.green)
					else:
						newItem.setBackground(QtCore.Qt.gray)
						
					self.ui.messageTable.setItem(row, 1, newItem)	

					row += 1
		
		self.ui.messageTable.setRowCount(row)
		self.ui.messageTable.setIconSize(QtCore.QSize(200,200))
		self.ui.messageTable.resizeColumnsToContents()
		self.ui.messageTable.setColumnWidth(1, 200)
		self.ui.messageTable.resizeRowsToContents()
		self.ui.messageTable.horizontalHeader().setStretchLastSection(True)

		# closing database
		tempdb.close()

def main(cursor, path):
	return SMSWidget(cursor, path)