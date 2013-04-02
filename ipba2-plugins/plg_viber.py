from PySide import QtCore, QtGui
from viber_ui import Ui_ViberBrowser

import os, sys, sqlite3, shutil, threading, webbrowser
from datetime import datetime
from collections import namedtuple

PLUGIN_NAME = "Viber Browser"
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

class ViBrowserWidget(QtGui.QWidget):
	
	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_ViberBrowser()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		self.fname_contacts = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename="Contacts.data", domaintype="AppDomain"))

		# check if files exist
		if (not os.path.isfile(self.fname_contacts)):
			raise Exception("Viber database not found: \"%s\""%self.fname_chatstorage)
		
		if (daemon == False):
			self.populateUI()

			# signal-slot chats/msgs connection
			QtCore.QObject.connect(self.ui.chatsWidget, QtCore.SIGNAL("itemSelectionChanged()"), self.onChatsClick)
			self.ui.chatsWidget.setColumnHidden(0,True)
			self.ui.msgsWidget.setColumnHidden(0,True)

			# signal-slot connection: right click context menu on contacts table
			self.ui.contactsWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			self.connect(self.ui.contactsWidget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenuContacts)	
			# signal-slot connection: right click context menu on calls table
			self.ui.callsWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			self.connect(self.ui.callsWidget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenuCalls)	
			# signal-slot connection: right click context menu on chats table
			self.ui.chatsWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			self.connect(self.ui.chatsWidget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenuChats)	
			# signal-slot connection: right click context menu on messages table
			self.ui.msgsWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			self.connect(self.ui.msgsWidget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenuMsgs)

	'''
	Populates the Viber Browser widget
	'''
	def populateUI(self):

		######################################################
		# CONTACTS SECTION                                   #
		######################################################
		
		contacts = self.getContacts()

		self.ui.contactsWidget.setRowCount(len(contacts))
		self.ui.contactsWidget.setSortingEnabled(False)
		
		row = 0
		for contact in contacts:
	
			if hasattr(contact, 'ZMAINNAME') and hasattr(contact, 'ZPREFIXNAME'):                                         
				newItem = QtGui.QTableWidgetItem()
				nameStr = ""
				if contact.ZPREFIXNAME is not None:
					nameStr += contact.ZPREFIXNAME + " "
				if contact.ZMAINNAME is not None:
					nameStr += contact.ZMAINNAME
				newItem.setData(QtCore.Qt.DisplayRole,nameStr)
				self.ui.contactsWidget.setItem(row, 0, newItem)
			if hasattr(contact, 'ZCANONIZEDPHONENUM'):                                         
				newItem = QtGui.QTableWidgetItem(str(contact.ZCANONIZEDPHONENUM))
				self.ui.contactsWidget.setItem(row, 1, newItem)                                       
			if hasattr(contact, 'ZREGISTRATIONDATE'):                                        
				newItem = QtGui.QTableWidgetItem()
				if contact.ZREGISTRATIONDATE is not None:
					newItem.setData(QtCore.Qt.DisplayRole,str(self.formatDate(contact.ZREGISTRATIONDATE)))
				self.ui.contactsWidget.setItem(row, 2, newItem)                                     
			if hasattr(contact, 'ZMODIFCATIONDATE'):                                        
				newItem = QtGui.QTableWidgetItem()
				if contact.ZMODIFCATIONDATE is not None:
					newItem.setData(QtCore.Qt.DisplayRole,str(self.formatDate(contact.ZMODIFCATIONDATE)))
				self.ui.contactsWidget.setItem(row, 3, newItem)
			if hasattr(contact, 'ZISVIBERICON') and hasattr(contact, 'ZICONID'):    			
				newItem = QtGui.QTableWidgetItem()

				iconRealFilename = ""
				iconlocalfile = ""
				if contact.ZISVIBERICON is 1 and contact.ZICONID is not None:
					iconlocalfile = contact.ZICONID + ".jpg"
					iconRealFilename = os.path.join(self.backup_path,
									plugins_utils.realFileName(self.cursor,
												   filename=iconlocalfile,
												   domaintype="AppDomain"))
					# add a thumnail to the table view
					icon = QtGui.QIcon(iconRealFilename)
					newItem.setIcon(icon)
				
					# add info for attachment export (ctx menu)
					newItem.setData(QtCore.Qt.UserRole, iconRealFilename)
					newItem.setData(QtCore.Qt.UserRole+1, iconlocalfile)
					
					self.ui.contactsWidget.setItem(row, 4, newItem)

			self.ui.contactsWidget.setRowHeight(row, 80)
			row = row + 1
	
		self.ui.contactsWidget.setSortingEnabled(True)
		self.ui.contactsWidget.setIconSize(QtCore.QSize(80,80))
		self.ui.contactsWidget.resizeColumnsToContents()
		self.ui.contactsWidget.setColumnWidth(4, 80)

		######################################################
		# RECENT CALLS SECTION                               #
		######################################################
		
		calls = self.getCalls()

		self.ui.callsWidget.setRowCount(len(calls))
		self.ui.callsWidget.setSortingEnabled(False)
		
		row = 0
		for call in calls:
	
			if hasattr(call, 'ZMAINNAME') and hasattr(call, 'ZPREFIXNAME'):                                         
				newItem = QtGui.QTableWidgetItem()
				nameStr = ""
				if call.ZPREFIXNAME is not None:
					nameStr += call.ZPREFIXNAME + " "
				if call.ZMAINNAME is not None:
					nameStr += call.ZMAINNAME
				newItem.setData(QtCore.Qt.DisplayRole,nameStr)
				self.ui.callsWidget.setItem(row, 0, newItem)                                    
			if hasattr(call, 'ZDATE'):                                        
				newItem = QtGui.QTableWidgetItem()
				if call.ZDATE is not None:
					newItem.setData(QtCore.Qt.DisplayRole,str(self.formatDate(call.ZDATE)))
				self.ui.callsWidget.setItem(row, 1, newItem)                                     
			if hasattr(call, 'ZDURATION'):
				newItem = QtGui.QTableWidgetItem()
				newItem.setData(QtCore.Qt.DisplayRole,call.ZDURATION)             
				self.ui.callsWidget.setItem(row, 2, newItem)
			if hasattr(call, 'ZCALLTYPE'):                                         
				newItem = QtGui.QTableWidgetItem(str(call.ZCALLTYPE))
				self.ui.callsWidget.setItem(row, 3, newItem)
				if 'missed' in str(call.ZCALLTYPE):
					for i in range(4):
						self.ui.callsWidget.item(row,i).setBackground(QtCore.Qt.red)
				elif 'incoming' in str(call.ZCALLTYPE):
					for i in range(4):
						self.ui.callsWidget.item(row,i).setBackground(QtCore.Qt.cyan)  
				else:
					for i in range(4):
						self.ui.callsWidget.item(row,i).setBackground(QtCore.Qt.green)

			row = row + 1
	
		self.ui.callsWidget.setSortingEnabled(True)	
		self.ui.callsWidget.resizeColumnsToContents()		
		self.ui.callsWidget.resizeRowsToContents()
		


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
			if hasattr(chat, 'ZMAINNAME') and hasattr(chat, 'ZPREFIXNAME'):                                         
				newItem = QtGui.QTableWidgetItem()
				nameStr = ""
				if chat.ZPREFIXNAME is not None:
					nameStr += chat.ZPREFIXNAME + " "
				if chat.ZMAINNAME is not None:
					nameStr += chat.ZMAINNAME
				newItem.setData(QtCore.Qt.DisplayRole,nameStr)
				self.ui.chatsWidget.setItem(row, 1, newItem) 
			if hasattr(chat, 'ZNAME'):                                         
				newItem = QtGui.QTableWidgetItem(chat.ZNAME)
				self.ui.chatsWidget.setItem(row, 2, newItem)                                       
			if hasattr(chat, 'ZGROUPID'):                                         
				newItem = QtGui.QTableWidgetItem(chat.ZGROUPID)
				self.ui.chatsWidget.setItem(row, 3, newItem)
			if hasattr(chat, 'ZDATE'):    
				newItem = QtGui.QTableWidgetItem(str(self.formatDate(chat.ZDATE)))
				self.ui.chatsWidget.setItem(row, 4, newItem)	
			if hasattr(chat, 'ZUNREADCOUNT'):    
				newItem = QtGui.QTableWidgetItem()
				newItem.setData(QtCore.Qt.DisplayRole,chat.ZUNREADCOUNT)
				self.ui.chatsWidget.setItem(row, 5, newItem)	
				
			if hasattr(chat, 'ZGROUPID'):
				if chat.ZGROUPID is not None:
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
	Function to fetch contacts related info
	'''
	def getContacts(self):

		# opening database
		try:          
			self.tempdb = sqlite3.connect(self.fname_contacts)
		except:
			print("\nUnexpected error: %s"%sys.exc_info()[1])
			self.close()

		# query results are retrieved as a namedtuple
		# (this step must be before cursor instantiation)
		self.tempdb.row_factory = namedtuple_factory                        	
		self.tempcur = self.tempdb.cursor()

		# ** ZABCONTACT - ZPHONENUMBERINDEX **
		zphonenumberindex_columns = "ZPHONENUMBERINDEX.Z_PK, ZPHONENUMBERINDEX.ZREGISTRATIONDATE, ZPHONENUMBERINDEX.ZCANONIZEDPHONENUM, ZPHONENUMBERINDEX.ZICONID"
		zabcontact_columns = "ZABCONTACT.ZISVIBERICON, ZABCONTACT.ZMODIFCATIONDATE, ZABCONTACT.ZMAINNAME, ZABCONTACT.ZPREFIXNAME"
		conditions = "ZPHONENUMBERINDEX.ZISVIBER = 1 AND ZPHONENUMBERINDEX.ZCONTACT = ZABCONTACT.Z_PK;"
		query = "SELECT " + zphonenumberindex_columns + ", " + zabcontact_columns + " FROM ZPHONENUMBERINDEX, ZABCONTACT WHERE " + conditions
		self.tempcur.execute(query)
		# fetches contacts namedtuple
		contacts = self.tempcur.fetchall()
			
		# closing database
		self.tempdb.close()

		# a namedtuple is returned		
		return contacts
		
	'''
	Function to fetch recent calls related info
	'''
	def getCalls(self):

		# opening database
		try:          
			self.tempdb = sqlite3.connect(self.fname_contacts)
		except:
			print("\nUnexpected error: %s"%sys.exc_info()[1])
			self.close()

		# query results are retrieved as a namedtuple
		# (this step must be before cursor instantiation)
		self.tempdb.row_factory = namedtuple_factory                        	
		self.tempcur = self.tempdb.cursor()

		# ** ZRECENT - ZRECENTSLINE ** -> ZPHONENUMBERINDEX -> ZABCONTACT
		zrecent_columns = "ZRECENT.ZDURATION, ZRECENT.ZDATE, ZRECENT.ZCALLTYPE"
		zabcontact_columns = "ZABCONTACT.ZMAINNAME, ZABCONTACT.ZPREFIXNAME"
		conditions = "ZRECENT.ZRECENTSLINE = ZRECENTSLINE.Z_PK AND ZRECENTSLINE.ZPHONENUMINDEX = ZPHONENUMBERINDEX.Z_PK AND ZPHONENUMBERINDEX.ZCONTACT = ZABCONTACT.Z_PK;"
		query = "SELECT " + zrecent_columns + ", " + zabcontact_columns + " FROM ZRECENT, ZRECENTSLINE, ZPHONENUMBERINDEX, ZABCONTACT WHERE " + conditions
		self.tempcur.execute(query)
		# fetches calls namedtuple
		calls = self.tempcur.fetchall()
			
		# closing database
		self.tempdb.close()

		# a namedtuple is returned		
		return calls
		
	'''
	Function to fetch conversations related info
	'''
	def getChats(self):

		# opening database
		try:    
			self.tempdb = sqlite3.connect(self.fname_contacts)
		except:
			print("\nUnexpected error: %s"%sys.exc_info()[1])
			self.close()
		
		# query results are retrieved as a namedtuple
		# (this step must be before cursor instantiation)
		self.tempdb.row_factory = namedtuple_factory                        	
		self.tempcur = self.tempdb.cursor()

		# ** ZCONVERSATION  ** -> Z_3PHONENUMINDEXES -> ZPHONENUMBERINDEX -> ZABCONTACT
		zconversation_columns = "ZCONVERSATION.Z_PK, ZCONVERSATION.ZDATE, ZCONVERSATION.ZUNREADCOUNT, ZCONVERSATION.ZGROUPID, ZCONVERSATION.ZNAME"
		zabcontact_columns = "ZABCONTACT.ZMAINNAME, ZABCONTACT.ZPREFIXNAME"
		conditions = "ZCONVERSATION.Z_PK = Z_3PHONENUMINDEXES.Z_3CONVERSATIONS AND Z_3PHONENUMINDEXES.Z_5PHONENUMINDEXES = ZPHONENUMBERINDEX.Z_PK AND ZPHONENUMBERINDEX.ZCONTACT = ZABCONTACT.Z_PK;"
		query = "SELECT " + zconversation_columns + ", " + zabcontact_columns + " FROM ZCONVERSATION, Z_3PHONENUMINDEXES, ZPHONENUMBERINDEX, ZABCONTACT WHERE " + conditions
		self.tempcur.execute(query)                
		# fetches chats namedtuple
		chats = self.tempcur.fetchall()
			
		# closing database
		self.tempdb.close()

		# a namedtuple is returned		
		return chats

	'''
	Function to fetch messages
	'''
	def getMsgs(self, zconversation):

		# refresh the window
		#(the selected row is highligthed and the chats table appears disabled)
		QtGui.QApplication.processEvents()

		# opening database
		try:    
			self.tempdb = sqlite3.connect(self.fname_contacts)
		except:
			print("\nUnexpected error: %s"%sys.exc_info()[1])
			self.close()
		
		# query results are retrieved as a namedtuple
		# (this step must be before cursor instantiation)
		self.tempdb.row_factory = namedtuple_factory                        	
		self.tempcur = self.tempdb.cursor()
				
		# ** ZVIBERMESSAGE ** - ZPHONENUMBERINDEX
		zvibermessage_columns = "ZVIBERMESSAGE.Z_PK, ZVIBERMESSAGE.ZATTACHMENT, ZVIBERMESSAGE.ZLOCATION, ZVIBERMESSAGE.ZPHONENUMINDEX, ZVIBERMESSAGE.ZDATE, ZVIBERMESSAGE.ZSTATEDATE, ZVIBERMESSAGE.ZSTATE, ZVIBERMESSAGE.ZTEXT"
		conditions = "ZVIBERMESSAGE.ZCONVERSATION=?;"
		query = "SELECT " + zvibermessage_columns + " FROM ZVIBERMESSAGE WHERE " + conditions
		self.tempcur.execute(query, [zconversation])
		messages = self.tempcur.fetchall()
		
		# closing database
		self.tempdb.close()

		# a namedtuple is returned		
		return messages
	
	'''
	Function to fetch messages (threaded)
	'''
	def getMsgsThreaded(self, zconversation):
		
		# progress window
		progress = QtGui.QProgressDialog("Querying the database ...", "Abort", 0, 0, self)
		progress.setWindowTitle("Viber Browser ...")
		progress.setWindowModality(QtCore.Qt.WindowModal)
		progress.setMinimumDuration(0)
		progress.setCancelButton(None)
		progress.show()
				
		# ** ZVIBERMESSAGE ** - ZPHONENUMBERINDEX
		zvibermessage_columns = "ZVIBERMESSAGE.Z_PK, ZVIBERMESSAGE.ZATTACHMENT, ZVIBERMESSAGE.ZLOCATION, ZVIBERMESSAGE.ZPHONENUMINDEX, ZVIBERMESSAGE.ZDATE, ZVIBERMESSAGE.ZSTATEDATE, ZVIBERMESSAGE.ZSTATE, ZVIBERMESSAGE.ZTEXT"
		conditions = "ZVIBERMESSAGE.ZCONVERSATION=?;"
		query = "SELECT " + zvibermessage_columns + " FROM ZVIBERMESSAGE WHERE " + conditions

		# call a thread to query the db showing a progress bar
		queryTh = ThreadedQuery(self.fname_contacts,query,[zconversation])
		queryTh.start()                
		while queryTh.isAlive():
			QtGui.QApplication.processEvents()

		progress.close()               
		messages = queryTh.getResult()
		
		# a namedtuple is returned		
		return messages

	'''
	Function to fetch msgs contact info
	'''
	def getMsgContact(self, zpk):

		# opening database
		try:    
			self.tempdb = sqlite3.connect(self.fname_contacts)
		except:
			print("\nUnexpected error: %s"%sys.exc_info()[1])
			self.close()
		
		# query results are retrieved as a namedtuple
		# (this step must be before cursor instantiation)
		self.tempdb.row_factory = namedtuple_factory                        	
		self.tempcur = self.tempdb.cursor()

		# ZPHONENUMBERINDEX - ZABCONTACT
		zphonenumberindex_columns = "ZPHONENUMBERINDEX.ZCANONIZEDPHONENUM"
		zabcontact_columns = "ZABCONTACT.ZMAINNAME, ZABCONTACT.ZPREFIXNAME"
		conditions = "ZPHONENUMBERINDEX.Z_PK=? AND ZPHONENUMBERINDEX.ZCONTACT = ZABCONTACT.Z_PK;"
		query = "SELECT " + zphonenumberindex_columns + ", " + zabcontact_columns + " FROM ZPHONENUMBERINDEX, ZABCONTACT WHERE " + conditions
		self.tempcur.execute(query, [zpk])
		msgcontact = self.tempcur.fetchone()
		
		# closing database
		self.tempdb.close()

		# a namedtuple is returned		
		return msgcontact

	'''
	Function to fetch location info
	'''
	def getLocation(self, zpk):

		# opening database
		try:    
			self.tempdb = sqlite3.connect(self.fname_contacts)
		except:
			print("\nUnexpected error: %s"%sys.exc_info()[1])
			self.close()
		
		# query results are retrieved as a namedtuple
		# (this step must be before cursor instantiation)
		self.tempdb.row_factory = namedtuple_factory                        	
		self.tempcur = self.tempdb.cursor()

		# ZVIBERLOCATION table
		query = "SELECT * FROM ZVIBERLOCATION WHERE Z_PK=?;"
		self.tempcur.execute(query, [zpk])
		location = self.tempcur.fetchone()
		
		# closing database
		self.tempdb.close()

		# a namedtuple is returned		
		return location

	'''
	Function to fetch attachment info
	'''
	def getMediaItem(self, zpk):

		# opening database
		try:    
			self.tempdb = sqlite3.connect(self.fname_contacts)
		except:
			print("\nUnexpected error: %s"%sys.exc_info()[1])
			self.close()
		
		# query results are retrieved as a namedtuple
		# (this step must be before cursor instantiation)
		self.tempdb.row_factory = namedtuple_factory                        	
		self.tempcur = self.tempdb.cursor()

		# ZATTACHMENT table
		query = "SELECT * FROM ZATTACHMENT WHERE Z_PK=?;"
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
		#msgs = self.getMsgs(zpk)               # <--- single thread
		msgs = self.getMsgsThreaded(zpk)        # <--- multithreaded

		# re-select a visible column to allow the keyboard selection
		self.ui.chatsWidget.setCurrentCell(self.ui.chatsWidget.currentRow(),1)

		# erase previous messages and set new table lenght
		#self.ui.msgsWidget.clearContents()
		self.ui.msgsWidget.setSortingEnabled(False)
		self.ui.msgsWidget.setRowCount(len(msgs))
		
		row = 0		
		for msg in msgs:

			from_me = False # var to remember from whom is the msg
	
			if hasattr(msg, 'Z_PK'):                                         
				newItem = QtGui.QTableWidgetItem()
				newItem.setData(QtCore.Qt.DisplayRole,msg.Z_PK)
				self.ui.msgsWidget.setItem(row, 0, newItem) 	
			if hasattr(msg, 'ZPHONENUMINDEX'):
				newItem = QtGui.QTableWidgetItem()
				fromstring = ""
				if msg.ZPHONENUMINDEX is not None:
					msgcontact = self.getMsgContact(msg.ZPHONENUMINDEX)
					if msgcontact is not None:
						if msgcontact.ZPREFIXNAME is not None:
							fromstring += msgcontact.ZPREFIXNAME + " "
						if msgcontact.ZMAINNAME is not None:
							fromstring += msgcontact.ZMAINNAME + " "
						if msgcontact.ZCANONIZEDPHONENUM is not None:
							fromstring += msgcontact.ZCANONIZEDPHONENUM
					else:
						fromstring = "N/A"
				else:
					fromstring = "Me"
					from_me = True
				newItem.setData(QtCore.Qt.DisplayRole,fromstring)
				self.ui.msgsWidget.setItem(row, 1, newItem)
			if hasattr(msg, 'ZDATE'):    
				newItem = QtGui.QTableWidgetItem(str(self.formatDate(msg.ZDATE)))
				self.ui.msgsWidget.setItem(row, 2, newItem)	
			if hasattr(msg, 'ZTEXT'):    			
				newItem = QtGui.QTableWidgetItem(msg.ZTEXT)
				self.ui.msgsWidget.setItem(row, 3, newItem)	
			if hasattr(msg, 'ZSTATE'):
				newItem = QtGui.QTableWidgetItem(msg.ZSTATE)
				self.ui.msgsWidget.setItem(row, 5, newItem)
			if hasattr(msg, 'ZSTATEDATE'):    
				newItem = QtGui.QTableWidgetItem(str(self.formatDate(msg.ZSTATEDATE)))
				self.ui.msgsWidget.setItem(row, 6, newItem)

			# ATTACHMENTS SECTION
						
			if hasattr(msg, 'ZATTACHMENT') and hasattr(msg, 'ZLOCATION'):
				
				mediaItem = QtGui.QTableWidgetItem("")

				msgcontent = ""

				# case 1: msg contains a location
				if msg.ZLOCATION is not None:
					location = self.getLocation(msg.ZLOCATION)
					msgcontent += "GPS\n" + "lat:  " + str(location.ZLATITUDE) + "\nlong: " + str(location.ZLONGITUDE) + "\naddress:  " + unicode(location.ZADDRESS) + "\n"

					# re-set message content (3rd column)
					newItem = QtGui.QTableWidgetItem(msgcontent)
					self.ui.msgsWidget.setItem(row, 3, newItem)

					# compose location thumbnail filename (guess)
					# example: if LAT = 41.796141 and LONG = 12.481714
					# the filename is 41.796141_12.jpg

					strlat = str(location.ZLATITUDE)
					strlong = str(location.ZLONGITUDE)
					strlat_s = strlat.split('.')
					strlong_s = strlong.split('.')
					filename = strlat_s[0] + "." + (strlat_s[1])[:6] + "_" + strlong_s[0] + ".jpg"

					locationlocalfile = filename
					locationRealFilename = os.path.join(self.backup_path,
									    plugins_utils.realFileName(self.cursor,
												       filename=locationlocalfile,
												       domaintype="AppDomain"))
					# add a thumbnail to the table view
					icon = QtGui.QIcon(locationRealFilename)
					mediaItem.setIcon(icon)
				
					# add info for attachment export (ctx menu)
					mediaItem.setData(QtCore.Qt.UserRole+2, location.ZLATITUDE)
					mediaItem.setData(QtCore.Qt.UserRole+3, location.ZLONGITUDE)
					

				# case 2: msg contains an attachment
				elif msg.ZATTACHMENT is not None:
					media = self.getMediaItem(msg.ZATTACHMENT)
					msgcontent += "ATTACHMENT\n" + "type:  " + str(media.ZTYPE) + "\nstate: " + str(media.ZSTATE) + "\nsize: " + str(media.ZFILESIZE) + "B\n"
					if 'sticker' in media.ZTYPE:
						msgcontent += "id: " + media.ZID + "\n"

					# re-set message content (3rd column)
					newItem = QtGui.QTableWidgetItem(msgcontent)
					self.ui.msgsWidget.setItem(row, 3, newItem)

					if media.ZNAME:
						medialocalfile = media.ZNAME
						mediaRealFilename = os.path.join(self.backup_path,
										 plugins_utils.realFileName(self.cursor,
													    filename=medialocalfile,
													    domaintype="AppDomain"))
						# add a thumbnail to the table view
						icon = QtGui.QIcon(mediaRealFilename)
						mediaItem.setIcon(icon)
					
						# add info for attachment export (ctx menu)
						mediaItem.setData(QtCore.Qt.UserRole, mediaRealFilename)
						mediaItem.setData(QtCore.Qt.UserRole+1, medialocalfile)
					
				self.ui.msgsWidget.setItem(row, 4, mediaItem)                                                

			if from_me:
				for i in range(7):
					self.ui.msgsWidget.item(row,i).setBackground(QtCore.Qt.green)
				
			row = row + 1
	
		self.ui.msgsWidget.setSortingEnabled(True)
		self.ui.msgsWidget.setIconSize(QtCore.QSize(150,150))
		self.ui.msgsWidget.resizeColumnsToContents()
		self.ui.msgsWidget.setColumnWidth(6, 150)	
		self.ui.msgsWidget.resizeRowsToContents()
		# signal-slot connection: preserve row height when sorting messages
		self.ui.msgsWidget.horizontalHeader().sortIndicatorChanged.connect(self.ui.msgsWidget.resizeRowsToContents)
		
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
		
		cell = self.ui.contactsWidget.itemAt(pos)
		if cell is not None:
			self.link = cell.data(QtCore.Qt.UserRole) 
			self.name = cell.data(QtCore.Qt.UserRole + 1)
		
		menu =  QtGui.QMenu()
		action1 = QtGui.QAction("Export table CSV", self)
		action1.triggered.connect(self.exportCSVcontacts)
		menu.addAction(action1)
		
		if self.link != None:

			menu.addSeparator()
				
			action1 = QtGui.QAction("Open contact icon in standard viewer", self)
			action1.triggered.connect(self.openWithViewer)
			menu.addAction(action1)
	
			action1 = QtGui.QAction("Export contact icon", self)
			action1.triggered.connect(self.exportSelectedFile)
			menu.addAction(action1)		

		menu.exec_(self.ui.contactsWidget.mapToGlobal(pos));
		
	
	def ctxMenuCalls(self, pos):
		
		menu =  QtGui.QMenu()
		action1 = QtGui.QAction("Export table CSV", self)
		action1.triggered.connect(self.exportCSVcalls)
		menu.addAction(action1)
		menu.exec_(self.ui.callsWidget.mapToGlobal(pos));
	
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
		
	def exportCSVcalls(self):
		self.exportCSVtable(self.ui.callsWidget)
		
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
	return ViBrowserWidget(cursor, path)

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
