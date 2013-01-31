# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
from whatsapp_ui import Ui_WhatsAppBrowser

import os, sqlite3
from datetime import datetime

PLUGIN_NAME = "WhatsApp Browser"
import plugins_utils

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
		
		if (daemon == False):
			self.populateUI()
		

	def populateUI(self):

                #reading contacts from database
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
		
	'''
	Contacts information are stored into Contacts.sqlite (newer version of WhatsApp for iOS)
	or into ChatStorage.sqlite.
	'''
	def getContacts(self):
                                
                try:
                        # opening database (1st attempt: Contacts.sqlite) << New Version
                        self.tempdb = sqlite3.connect(self.fname_contacts)
                        has_contacts_sqlite = True
                except:
                        # opening database (2nd attempt: ChatStorage.sqlite) << Old Version
                        self.tempdb = sqlite3.connect(self.fname_chatstorage)
                        has_contacts_sqlite = False
                        
		self.tempdb.row_factory = sqlite3.Row
		self.tempcur = self.tempdb.cursor()
		
		contactsToReturn = []

                if has_contacts_sqlite:
                        
                        # reading contacts from database
                        # 1st step: ZWAPHONE table
                        query = "SELECT * FROM ZWAPHONE"
                        self.tempcur.execute(query)
                        contacts = self.tempcur.fetchall()

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

                # TODO
                # TODO
		
		chatsToReturn = []
		
                # TODO
                # TODO
		
		return contactsToReturn

                

	def formatDate(self, mactime):
                # if timestamp is not like "304966548", but like "306350664.792749",
                # then just use the numbers in front of the "."
                mactime = str(mactime)
                if mactime.find(".") > -1:
                        mactime = mactime[:mactime.find(".")]
                date_time = datetime.fromtimestamp(int(mactime)+11323*60*1440)
                return date_time
                

	def setTitle(self, title):
		self.setWindowTitle(title)

def main(cursor, path):
	return WABrowserWidget(cursor, path)

def report(cursor, path):
	
	returnString = ""

	waBrowser = WABrowserWidget(cursor, path, daemon = True)
	contacts = waBrowser.getContacts()
	del waBrowser


        # main title
	returnString += "<h1>iPBA WhatsApp Browser</h1>\n"

	# 1st Table - Contacts
	returnString += "<h2>Contacts</h2>\n"
	
	returnString += '<table class="sortable" id="chatsession" border="1" cellpadding="2" cellspacing="0">\n'
	returnString += '<thead>'
	returnString += '<tr><th>Name</th><th>Phone Number</th><th>Status Text</th><th>Status Date</th></tr>\n'
	returnString += '</thead>'

	
	returnString += '</tbody>'
	for contact in contacts:

		returnString += "<tr>"
		returnString += ("<td>%s</td>"%contact[1]).encode('utf-8')
		returnString += ("<td>%s</td>"%contact[2]).encode('utf-8')
		returnString += ("<td>%s</td>"%contact[3]).encode('utf-8')
		returnString += ("<td>%s</td>"%contact[4]).encode('utf-8')
		returnString += "</tr>\n"
	
	returnString += '</tbody>'
	returnString += "</table>"

	# 2nd Table - Chat Sessions
	returnString += "<h2>Chat Sessions</h2>\n"

	# TODO
	# TODO

	# 3rd Table - Messages
	returnString += "<h2>Messages</h2>\n"
	
	# TODO
	# TODO

        
	return returnString
