from PySide import QtCore, QtGui
from whatsapp_ui import Ui_WhatsAppBrowser

import os, sys, sqlite3, shutil, threading, webbrowser
from datetime import datetime
from collections import namedtuple

PLUGIN_NAME = "WhatsApp Browser"
import plugins_utils

################################################################################
class ThreadedQuery(threading.Thread):
	def __init__(self, dbfname, querystring, queryparams):
		threading.Thread.__init__(self)
		self._dbfname = dbfname
		self._querystring = querystring
		self._queryparams = queryparams
		self._result = None
		
	def run(self):
		try:
			# opens database
			tempdb = sqlite3.connect(self._dbfname)
		
			# query results are retrieved as a namedtuple
			# (this step must be before cursor instantiation)
			tempdb.row_factory = namedtuple_factory                        	
			tempcur = tempdb.cursor()

			
			if self._queryparams is None:
				tempcur.execute(self._querystring)
			else:
				tempcur.execute(self._querystring, self._queryparams)
				
			# fetches results
			self._result = tempcur.fetchall()
			
			# closing database
			tempdb.close()
			
		except:                        
			print("\nUnexpected error: %s"%sys.exc_info()[1])
			
	def getResult(self):
		return self._result
################################################################################

class WABrowserWidget(QtGui.QWidget):
	
	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_WhatsAppBrowser()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		self.fname_contacts = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename="Contacts.sqlite", domaintype="AppDomain"))
		self.fname_chatstorage = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename="ChatStorage.sqlite", domaintype="AppDomain"))

		# check if files exist
		if (not os.path.isfile(self.fname_chatstorage)):
			raise Exception("WhatsApp database not found: \"%s\""%self.fname_chatstorage)
		
		if (daemon == False):
			self.populateUI()

			# signal-slot chats/msgs connection
			QtCore.QObject.connect(self.ui.chatsWidget, QtCore.SIGNAL("itemSelectionChanged()"), self.onChatsClick)
			self.ui.chatsWidget.setColumnHidden(0,True)
			self.ui.msgsWidget.setColumnHidden(0,True)
						
			# signal-slot connection: right click context menu on contacts table
			self.ui.contactsWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			self.connect(self.ui.contactsWidget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenuContacts)	
			# signal-slot connection: right click context menu on chats table
			self.ui.chatsWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			self.connect(self.ui.chatsWidget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenuChats)	
			# signal-slot connection: right click context menu on messages table
			self.ui.msgsWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			self.connect(self.ui.msgsWidget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenuMsgs)	
	'''
	Populates the WhatsApp Browser widget
	'''
	def populateUI(self):

		######################################################
		# CONTACTS SECTION                                   #
		######################################################
		
		contacts = self.getContacts()		

		self.ui.contactsWidget.setRowCount(len(contacts))
		
		row = 0
		for contact in contacts:

			id = contact[0]
			name = contact[1]
			phonenum = contact[2]
			text = contact[3]
			date = contact[4]

			newItem = QtGui.QTableWidgetItem(name)
			self.ui.contactsWidget.setItem(row, 0, newItem)				
			newItem = QtGui.QTableWidgetItem(phonenum)
			self.ui.contactsWidget.setItem(row, 1, newItem)	
			newItem = QtGui.QTableWidgetItem(text)
			self.ui.contactsWidget.setItem(row, 2, newItem)	
			newItem = QtGui.QTableWidgetItem(str(date))
			self.ui.contactsWidget.setItem(row, 3, newItem)	
			
			row = row + 1
	
		self.ui.contactsWidget.resizeColumnsToContents()		
		self.ui.contactsWidget.resizeRowsToContents()


		######################################################
		# CHATS SECTION                                      #
		######################################################
		
		chats = self.getChats()
		
		self.ui.chatsWidget.setRowCount(len(chats))
		
		row = 0		
		for chat in chats:
	
			if hasattr(chat, 'Z_PK'):                                         
				newItem = QtGui.QTableWidgetItem()
				newItem.setData(QtCore.Qt.DisplayRole,chat.Z_PK)
				self.ui.chatsWidget.setItem(row, 0, newItem)
			if hasattr(chat, 'ZPARTNERNAME'):                                         
				newItem = QtGui.QTableWidgetItem(chat.ZPARTNERNAME)
				self.ui.chatsWidget.setItem(row, 1, newItem)                                       
			if hasattr(chat, 'ZCONTACTJID'):                                         
				newItem = QtGui.QTableWidgetItem(chat.ZCONTACTJID)
				self.ui.chatsWidget.setItem(row, 2, newItem)
			if hasattr(chat, 'ZMESSAGECOUNTER'):    			
				newItem = QtGui.QTableWidgetItem()
				newItem.setData(QtCore.Qt.DisplayRole,chat.ZMESSAGECOUNTER-1)
				self.ui.chatsWidget.setItem(row, 3, newItem)	
			if hasattr(chat, 'ZUNREADCOUNT'):    
				newItem = QtGui.QTableWidgetItem()
				newItem.setData(QtCore.Qt.DisplayRole,chat.ZUNREADCOUNT)
				self.ui.chatsWidget.setItem(row, 4, newItem)	
			if hasattr(chat, 'ZLASTMESSAGEDATE'):    
				newItem = QtGui.QTableWidgetItem(str(self.formatDate(chat.ZLASTMESSAGEDATE)))
				self.ui.chatsWidget.setItem(row, 5, newItem)
				
			if hasattr(chat, 'ZGROUPINFO'):
				if chat.ZGROUPINFO is not None:
					for i in range(6):
						self.ui.chatsWidget.item(row,i).setBackground(QtCore.Qt.yellow)  
			
			row = row + 1
	
		self.ui.chatsWidget.resizeColumnsToContents()		
		self.ui.chatsWidget.resizeRowsToContents()
		
			
	def formatDate(self, mactime):
		# if timestamp is not like "304966548", but like "306350664.792749",
		# then just use the numbers in front of the "."
		mactime = str(mactime)
		if mactime.find(".") > -1:
			mactime = mactime[:mactime.find(".")]
		date_time = datetime.fromtimestamp(int(mactime)+11323*60*1440)
		return date_time

	
	########################################################################
	# DB QUERIES                                                           #
	########################################################################
		
	'''
	Contacts information are stored into Contacts.sqlite (newer version of WhatsApp for iOS)
	or into ChatStorage.sqlite.
	'''
	def getContacts(self):

		try:              
			try:
				# opening database (1st attempt: Contacts.sqlite) << New Version
				self.tempdb = sqlite3.connect(self.fname_contacts)
				has_contacts_sqlite = True
			except:
				# opening database (2nd attempt: ChatStorage.sqlite) << Old Version
				self.tempdb = sqlite3.connect(self.fname_chatstorage)
				has_contacts_sqlite = False
		except:
			print("\nUnexpected error: %s"%sys.exc_info()[1])
			self.close()
			
		self.tempdb.row_factory = sqlite3.Row
		self.tempcur = self.tempdb.cursor()
		
		contactsToReturn = []

		if has_contacts_sqlite:
			
			# reading contacts from database
			# 1st step: ZWAPHONE table
			query = "SELECT * FROM ZWAPHONE"
			self.tempcur.execute(query)
			contacts = self.tempcur.fetchall()
			
			readCount = 0
			for contact in contacts:
				id = contact['Z_PK']
				contact_key = contact['ZCONTACT']
				favorite_key = contact['ZFAVORITE']
				status_key = contact['ZSTATUS']
				phonenum = contact['ZPHONE']

				# 2nd step: name from ZWACONTACT table
				query = "SELECT * FROM ZWACONTACT WHERE Z_PK=?;"
				self.tempcur.execute(query, [contact_key])
				contact_entry = self.tempcur.fetchone()
				if contact_entry == None:
					name = "N/A"
				else:
					name = contact_entry['ZFULLNAME']

				# 3rd step: status from ZWASTATUS table
				query = "SELECT * FROM ZWASTATUS WHERE Z_PK=?;"
				self.tempcur.execute(query, [status_key])
				status_entry = self.tempcur.fetchone()
				if status_entry == None:
					text = "N/A"
					date = "N/A"
				else:
					text = status_entry['ZTEXT']
					date = self.formatDate(status_entry['ZDATE'])
			
				contactsToReturn.append([id, name, phonenum, text, date])
					
		else: # has_contacts_sqlite == False
			
			# reading contacts from database
			# 1st step: ZWAPHONE table
			query = "SELECT * FROM ZWAFAVORITE"
			self.tempcur.execute(query)
			contacts = self.tempcur.fetchall()

			for contact in contacts:
				id = contact['Z_PK']
				status_key = contact['ZSTATUS']
				name = contact['ZDISPLAYNAME']
				phonenum = contact['ZPHONENUMBER']

				# 2nd step: status from ZWASTATUS table
				query = "SELECT * FROM ZWASTATUS WHERE Z_PK=?;"
				self.tempcur.execute(query, [status_key])
				status_entry = self.tempcur.fetchone()
				if status_entry == None:
					text = "N/A"
					date = "N/A"
				else:
					text = status_entry['ZSTATUSTEXT']
					date = self.formatDate(status_entry['ZSTATUSDATE'])
			
				contactsToReturn.append([id, name, phonenum, text, date])
			
		# closing database
		self.tempdb.close()
		
		return contactsToReturn
		
	'''
	Chats information are stored into ChatStorage.sqlite.
	'''
	def getChats(self):

		# opens database (ChatStorage.sqlite)
		try:    
			self.tempdb = sqlite3.connect(self.fname_chatstorage)
		except:
			print("\nUnexpected error: %s"%sys.exc_info()[1])
			self.close()
		
		# query results are retrieved as a namedtuple
		# (this step must be before cursor instantiation)
		self.tempdb.row_factory = namedtuple_factory                        	
		self.tempcur = self.tempdb.cursor()

		# ZWACHATSESSION table
		query = "SELECT * FROM ZWACHATSESSION"
		self.tempcur.execute(query)                
		# fetches chats namedtuple
		chats = self.tempcur.fetchall()
			
		# closing database
		self.tempdb.close()

		# a namedtuple is returned		
		return chats

	'''
	Messages are stored into ChatStorage.sqlite.
	'''
	def getMsgs(self, zchatsession):

		# refresh the window
		#(the selected row is highligthed and the chats table appears disabled)
		QtGui.QApplication.processEvents()

		# opens database (ChatStorage.sqlite)
		try:    
			self.tempdb = sqlite3.connect(self.fname_chatstorage)
		except:
			print("\nUnexpected error: %s"%sys.exc_info()[1])
			self.close()
		
		# query results are retrieved as a namedtuple
		# (this step must be before cursor instantiation)
		self.tempdb.row_factory = namedtuple_factory                        	
		self.tempcur = self.tempdb.cursor()
				
		# ZWAMESSAGE table
		query = "SELECT * FROM ZWAMESSAGE WHERE ZCHATSESSION=? ORDER BY ZMESSAGEDATE ASC;"
		self.tempcur.execute(query, [zchatsession])
		messages = self.tempcur.fetchall()
		
		# closing database
		self.tempdb.close()

		# a namedtuple is returned		
		return messages
	
	'''
	Messages are stored into ChatStorage.sqlite.
	'''
	def getMsgsThreaded(self, zchatsession):
		
		# progress window
		progress = QtGui.QProgressDialog("Querying the database ...", "Abort", 0, 0, self)
		progress.setWindowTitle("WhatsApp Browser ...")
		progress.setWindowModality(QtCore.Qt.WindowModal)
		progress.setMinimumDuration(0)
		progress.setCancelButton(None)
		progress.show()
				
		# ZWAMESSAGE table
		query = "SELECT * FROM ZWAMESSAGE WHERE ZCHATSESSION=? ORDER BY ZMESSAGEDATE ASC;"

		# call a thread to query the db showing a progress bar
		queryTh = ThreadedQuery(self.fname_chatstorage,query,[zchatsession])
		queryTh.start()                
		while queryTh.isAlive():
			QtGui.QApplication.processEvents()

		progress.close()               
		messages = queryTh.getResult()
		
		# a namedtuple is returned		
		return messages

	'''
	GroupMember info are stored into ChatStorage.sqlite.
	'''
	def getGroupInfo(self, zpk):

		# opens database (ChatStorage.sqlite)
		try:    
			self.tempdb = sqlite3.connect(self.fname_chatstorage)
		except:
			print("\nUnexpected error: %s"%sys.exc_info()[1])
			self.close()
		
		# query results are retrieved as a namedtuple
		# (this step must be before cursor instantiation)
		self.tempdb.row_factory = namedtuple_factory                        	
		self.tempcur = self.tempdb.cursor()

		# ZWAGROUPMEMBER table
		query = "SELECT * FROM ZWAGROUPMEMBER WHERE Z_PK=?;"
		self.tempcur.execute(query, [zpk])
		groupmember = self.tempcur.fetchone()
		
		# closing database
		self.tempdb.close()

		# a namedtuple is returned		
		return groupmember

	'''
	MediaItem info are stored into ChatStorage.sqlite.
	'''
	def getMediaItem(self, zpk):

		# opens database (ChatStorage.sqlite)
		try:    
			self.tempdb = sqlite3.connect(self.fname_chatstorage)
		except:
			print("\nUnexpected error: %s"%sys.exc_info()[1])
			self.close()
		
		# query results are retrieved as a namedtuple
		# (this step must be before cursor instantiation)
		self.tempdb.row_factory = namedtuple_factory                        	
		self.tempcur = self.tempdb.cursor()

		# ZMEDIAITEM table
		query = "SELECT * FROM ZWAMEDIAITEM WHERE Z_PK=?;"
		self.tempcur.execute(query, [zpk])
		media = self.tempcur.fetchone()
		
		# closing database
		self.tempdb.close()

		# a namedtuple is returned		
		return media

	########################################################################
	# SLOTS                                                                #
	########################################################################        

	def onChatsClick(self):

		# disable chats table (to disable click events while processing)
		self.ui.chatsWidget.setEnabled(False)
		
		# retrieving selected row
		self.ui.chatsWidget.setCurrentCell(self.ui.chatsWidget.currentRow(),0)
		currentSelectedItem = self.ui.chatsWidget.currentItem()
		if (currentSelectedItem): pass
		else: return

		######################################################
		# MESSAGES SECTION                                   #
		######################################################

		zpk = int(currentSelectedItem.text())
		#msgs = self.getMsgs(zpk)               # <---
		msgs = self.getMsgsThreaded(zpk)        # <---

		# re-select a visible column to allow the keyboard selection
		self.ui.chatsWidget.setCurrentCell(self.ui.chatsWidget.currentRow(),1)

		# erase previous messages and set new table lenght
		#self.ui.msgsWidget.clearContents()
		self.ui.msgsWidget.setSortingEnabled(False)
		self.ui.msgsWidget.setRowCount(len(msgs))
		
		row = 0		
		for msg in msgs:               
	
			if hasattr(msg, 'Z_PK'):                                         
				newItem = QtGui.QTableWidgetItem()
				newItem.setData(QtCore.Qt.DisplayRole,msg.Z_PK)
				self.ui.msgsWidget.setItem(row, 0, newItem) 	
			if hasattr(msg, 'ZFROMJID'):
				fromstring = "Me"
				if msg.ZFROMJID is not None:
					fromstring = msg.ZFROMJID
				newItem = QtGui.QTableWidgetItem()
				newItem.setData(QtCore.Qt.DisplayRole,fromstring)
				self.ui.msgsWidget.setItem(row, 1, newItem)
			if hasattr(msg, 'ZMESSAGEDATE'):    
				newItem = QtGui.QTableWidgetItem(str(self.formatDate(msg.ZMESSAGEDATE)))
				self.ui.msgsWidget.setItem(row, 2, newItem)	
			if hasattr(msg, 'ZTEXT'):    			
				newItem = QtGui.QTableWidgetItem(msg.ZTEXT)
				self.ui.msgsWidget.setItem(row, 3, newItem)	
			if hasattr(msg, 'ZMESSAGESTATUS'):    
				newItem = QtGui.QTableWidgetItem()
				newItem.setData(QtCore.Qt.DisplayRole,msg.ZMESSAGESTATUS)
				self.ui.msgsWidget.setItem(row, 5, newItem)
						
			if hasattr(msg, 'ZGROUPMEMBER'):
				if msg.ZGROUPMEMBER is not None:
					gmember = self.getGroupInfo(msg.ZGROUPMEMBER)
					fromstring = ""
					if gmember is not None:
						fromstring = gmember.ZCONTACTNAME + " - " + gmember.ZMEMBERJID 
					else:
						fromstring = "N/A"
					newItem = QtGui.QTableWidgetItem(fromstring)
					self.ui.msgsWidget.setItem(row, 1, newItem)
						
			if hasattr(msg, 'ZMEDIAITEM'):                                
				mediaItem = QtGui.QTableWidgetItem("")                                
				if msg.ZMEDIAITEM is not None:
					media = self.getMediaItem(msg.ZMEDIAITEM)
					msgcontent = ""
					# VCARD info
					if (media.ZVCARDNAME and media.ZVCARDSTRING) is not None:
						msgcontent += ("VCARD\n" + media.ZVCARDNAME + "\n" + media.ZVCARDSTRING + "\n")
					# GPS info
					if media.ZLATITUDE != 0. or media.ZLONGITUDE != 0.:
						msgcontent += ("GPS\n" + "lat:  " + str(media.ZLATITUDE) + "\nlong: " + str(media.ZLONGITUDE) + "\n")
					# VIDEO info
					if media.ZMOVIEDURATION != 0:
						msgcontent += ("VIDEO\n" + "duration: " + str(media.ZMOVIEDURATION) + " sec\n")
					# FILE info
					if media.ZFILESIZE != 0:
						msgcontent += ("FILE\n" + "size: " + str(media.ZFILESIZE) + " B\n")

					# set message content (3rd column)
					newItem = QtGui.QTableWidgetItem(msgcontent)
					self.ui.msgsWidget.setItem(row, 3, newItem)

					thumbRealFilename = ""
					mediaRealFilename = ""
					mediallocalfile = ""
						
					# THUMBNAIL
					if media.ZTHUMBNAILLOCALPATH is not None:                                                                                            
						thumblocalfilepath = media.ZTHUMBNAILLOCALPATH
						thumblocalpath = os.path.dirname(thumblocalfilepath)
						thumbllocalfile = os.path.basename(thumblocalfilepath)
						thumbRealFilename = os.path.join(self.backup_path,
										 plugins_utils.realFileName(self.cursor,
													    filename=thumbllocalfile,
													    path='Library/'+thumblocalpath,
													    domaintype="AppDomain"))
					# ATTACHMENT
					if media.ZMEDIALOCALPATH is not None:
						medialocalfilepath = media.ZMEDIALOCALPATH
						mediallocalpath = os.path.dirname(medialocalfilepath)
						mediallocalfile = os.path.basename(medialocalfilepath)
						mediaRealFilename = os.path.join(self.backup_path,
										 plugins_utils.realFileName(self.cursor,
													    filename=mediallocalfile,
													    path='Library/'+mediallocalpath,
													    domaintype="AppDomain"))
					# add a thumnail to the table view
					icon = None
					if thumbRealFilename != "":
						icon = QtGui.QIcon(thumbRealFilename)
					else:
						icon = QtGui.QIcon(mediaRealFilename)
					mediaItem = QtGui.QTableWidgetItem()
					mediaItem.setIcon(icon)
					
					# add info for attachment export (ctx menu)
					if mediallocalfile != "":
						mediaItem.setData(QtCore.Qt.UserRole, mediaRealFilename)
						mediaItem.setData(QtCore.Qt.UserRole+1, mediallocalfile)
					if media.ZLATITUDE != 0. or media.ZLONGITUDE != 0.:
						mediaItem.setData(QtCore.Qt.UserRole+2, media.ZLATITUDE)
						mediaItem.setData(QtCore.Qt.UserRole+3, media.ZLONGITUDE)
						
				self.ui.msgsWidget.setItem(row, 4, mediaItem)                                                

			if hasattr(msg, 'ZISFROMME'):
				if msg.ZISFROMME is 1:
					for i in range(6):
						self.ui.msgsWidget.item(row,i).setBackground(QtCore.Qt.green)
				
			row = row + 1
	
		self.ui.msgsWidget.setSortingEnabled(True)
		self.ui.msgsWidget.setIconSize(QtCore.QSize(150,150))
		self.ui.msgsWidget.resizeColumnsToContents()
		self.ui.msgsWidget.setColumnWidth(4, 150)	
		self.ui.msgsWidget.resizeRowsToContents()
		
		# re-enable chats table
		self.ui.chatsWidget.setEnabled(True)
		self.ui.chatsWidget.setFocus()

		
	######################################################
	# CTX MENU SECTION                                   #
	######################################################
	
	def ctxMenuMsgs(self, pos):	

		cell = self.ui.msgsWidget.itemAt(pos)
		self.link = cell.data(QtCore.Qt.UserRole) 
		self.name = cell.data(QtCore.Qt.UserRole + 1)
		self.lat  = cell.data(QtCore.Qt.UserRole + 2) 
		self.long = cell.data(QtCore.Qt.UserRole + 3)
		
		menu =  QtGui.QMenu()
		
		action1 = QtGui.QAction("Export table CSV", self)
		action1.triggered.connect(self.exportCSVmsgs)
		menu.addAction(action1)
		
		if self.link != None:

			menu.addSeparator()
				
			action1 = QtGui.QAction("Open attachment in standard viewer", self)
			action1.triggered.connect(self.openWithViewer)
			menu.addAction(action1)
	
			action1 = QtGui.QAction("Export attachment", self)
			action1.triggered.connect(self.exportSelectedFile)
			menu.addAction(action1)

		if (self.lat and self.long) is not None:

			menu.addSeparator()
				
			action1 = QtGui.QAction("Show GPS coordinates on Google Maps", self)
			action1.triggered.connect(self.openGPSBrowser)
			menu.addAction(action1)		

		menu.exec_(self.ui.msgsWidget.mapToGlobal(pos));
		
	
	def ctxMenuContacts(self, pos):
		
		menu =  QtGui.QMenu()
		action1 = QtGui.QAction("Export table CSV", self)
		action1.triggered.connect(self.exportCSVcontacts)
		menu.addAction(action1)
		menu.exec_(self.ui.contactsWidget.mapToGlobal(pos));
	
	def ctxMenuChats(self, pos):
		
		menu =  QtGui.QMenu()
		action1 = QtGui.QAction("Export table CSV", self)
		action1.triggered.connect(self.exportCSVchats)
		menu.addAction(action1)
		menu.exec_(self.ui.chatsWidget.mapToGlobal(pos));

	##### ATTACHMENTS EXPORT FUNCTIONS #####
	
	def openWithViewer(self):

		if sys.platform.startswith('linux'):
			subprocess.call(["xdg-open", self.link])
		else:
			os.startfile(self.link)

	def exportSelectedFile(self):
	
		filename = QtGui.QFileDialog.getSaveFileName(self, "Export attachment", self.name)		
		filename = filename[0]
		
		if (len(filename) == 0):
			return
		
		try:
			shutil.copy(self.link, filename)
			QtGui.QMessageBox.about(self, "Confirm", "Attachment saved as %s."%filename)
		except:
			QtGui.QMessageBox.about(self, "Error", "Error while saving attachment")
	
	def openGPSBrowser(self):
		coordinatesURL = "https://maps.google.com/?q=" + str(self.lat) + "," + str(self.long)
		webbrowser.open(coordinatesURL)

	##### TABLES EXPORT FUNCTIONS #####	

	def exportCSVcontacts(self):
		self.exportCSVtable(self.ui.contactsWidget)
		
	def exportCSVchats(self):
		self.exportCSVtable(self.ui.chatsWidget)
		
	def exportCSVmsgs(self):
		self.exportCSVtable(self.ui.msgsWidget)

	def exportCSVtable(self, table):
	
		filename = QtGui.QFileDialog.getSaveFileName(self, "Export table", "table", ".csv")		
		filename = filename[0]
		
		if (len(filename) == 0):
			return

		f = open(filename, 'w')
		
		# header
		tablerow='"'
		for c in range(table.columnCount()):
			hitem = table.horizontalHeaderItem(c)
			if hitem is not None:
				tablerow += unicode(hitem.text()).encode('utf8')
			tablerow += '","'
		tablerow=tablerow[:-2]+"\n"
		f.write(tablerow)

		# content
		tablerow='"'
		for r in range(table.rowCount()):
			for c in range(table.columnCount()):
				item = table.item(r,c)
				if item is not None:
					tablerow += unicode(item.text().replace('\n',' ')).encode('utf8')
				tablerow += '","'
			tablerow = tablerow[:-2] + "\n"
			f.write(tablerow)
			tablerow='"'
		f.close()
	

################################################################################
################################################################################

def main(cursor, path):
	return WABrowserWidget(cursor, path)

##def report(cursor, path):
##	
##	returnString = ""
##
##	waBrowser = WABrowserWidget(cursor, path, daemon = True)
##	contacts = waBrowser.getContacts()
##	del waBrowser
##
##
##        # main title
##	returnString += "<h1>iPBA WhatsApp Browser</h1>\n"
##
##	# 1st Table - Contacts
##	returnString += "<h2>Contacts</h2>\n"
##	
##	returnString += '<table class="sortable" id="contacts" border="1" cellpadding="2" cellspacing="0">\n'
##	returnString += '<thead>'
##	returnString += '<tr><th>Name</th><th>Phone Number</th><th>Status Text</th><th>Status Date</th></tr>\n'
##	returnString += '</thead>'
##
##	
##	returnString += '</tbody>'
##	for contact in contacts:
##
##		returnString += "<tr>"
##		returnString += ("<td>%s</td>"%contact[1]).encode('utf-8')
##		returnString += ("<td>%s</td>"%contact[2]).encode('utf-8')
##		returnString += ("<td>%s</td>"%contact[3]).encode('utf-8')
##		returnString += ("<td>%s</td>"%contact[4]).encode('utf-8')
##		returnString += "</tr>\n"
##	
##	returnString += '</tbody>'
##	returnString += "</table>"
##
##	# 2nd Table - Chat Sessions
##	returnString += "<h2>Chat Sessions</h2>\n"
##
##	# TODO
##	# TODO
##
##	# 3rd Table - Messages
##	returnString += "<h2>Messages</h2>\n"
##	
##	# TODO
##	# TODO
##
##        
##	return returnString

'''
Namedtuple factory
http://peter-hoffmann.com/2010/python-sqlite-namedtuple-factory.html
'''
def namedtuple_factory(cursor, row):
	"""
	Usage:
	con.row_factory = namedtuple_factory
	"""
	fields = [col[0] for col in cursor.description]
	Row = namedtuple("Row", fields)
	return Row(*row)
