from PySide import QtCore, QtGui
from addressbook_ui import Ui_AddressBook

import os, sqlite3, sys
from datetime import datetime
from string import *

PLUGIN_NAME = "Address Book"
import plugins_utils

# retrieve modules from ipba root directory
import plistutils

class AddressBookWidget(QtGui.QWidget):

	def clearHtml(self, text):
		if (text == None):
			text = "<None>"
		return text.encode('ascii', "xmlcharrefreplace")
	
	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_AddressBook()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		self.filename = os.path.join(self.backup_path, plugins_utils.realFileName(cursor, filename="AddressBook.sqlitedb", domaintype="HomeDomain"))
		self.thumbsfilename = os.path.join(self.backup_path, plugins_utils.realFileName(cursor, filename="AddressBookImages.sqlitedb", domaintype="HomeDomain"))		

		# check if files exist
		if (not os.path.isfile(self.filename)):
			raise Exception("Contacts database not found: \"%s\""%self.filename)
		if (not os.path.isfile(self.thumbsfilename)):
			self.thumbsfilename = None
			
		if (daemon == False):
			self.populateUI()
	
	def retrieveGroups(self):
	
		# opening database
		self.tempdb = sqlite3.connect(self.filename)
		self.tempdb.row_factory = sqlite3.Row
		self.tempcur = self.tempdb.cursor() 
		
		contacts = []
		
		# all contacts
		allContacts = []
		query = "SELECT ROWID, First, Last, Organization FROM ABPerson ORDER BY Last, First, Organization"
		self.tempcur.execute(query)
		people = self.tempcur.fetchall()
		for person in people:
			personid = person['ROWID']
			
			name = ""
			if (person['First'] != None):
				name = person['First'] + " "
			if (person['Last'] != None):
				name = name + person['Last']
			if (person['First'] == None and person['Last'] == None):
				name = person['Organization']
			
			if (name == None):
				name = "<None>"
			
			allContacts.append([personid, name])

		contacts.append(["All Contacts", allContacts])
		
		# groups contacts
		query = "SELECT ROWID, Name FROM ABGroup"
		self.tempcur.execute(query)
		groups = self.tempcur.fetchall()
		
		for group in groups:
			groupid = group[0]
			groupname = group[1]

			query = "SELECT ABPerson.ROWID, First, Last, Organization FROM ABGroupMembers INNER JOIN ABPerson ON ABGroupMembers.member_id = ABPerson.ROWID WHERE ABGroupMembers.group_id = \"%s\" ORDER BY Last, First, Organization"%groupid
			self.tempcur.execute(query)
			people = self.tempcur.fetchall()
			
			groupContacts = []
			for person in people:
				personid = person[0]
				
				if (person[1] != None):
					name = person[1]
				if (person[2] != None):
					name = name + " " + person[2]
				if (person[1] == None and person[2] == None):
					name = person[3]
					
				if (name == None):
					name = "<None>"
					
				groupContacts.append([personid, name])
	
			contacts.append([groupname, groupContacts])		

		self.tempdb.close()
		
		return contacts

					
	def populateUI(self):
	
		QtCore.QObject.connect(self.ui.contactsTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onContactClick)
		self.ui.contactsTree.setColumnHidden(1,True)
		
		self.ui.imageLabel.hide()
	
		contacts = self.retrieveGroups()
		
		for group in contacts:
			groupName = str(group[0].encode("utf-8"))
			groupContacts = group[1]
			
			groupNode = QtGui.QTreeWidgetItem(None)
			groupNode.setText(1, "")
			groupNode.setText(0, groupName)
			self.ui.contactsTree.addTopLevelItem(groupNode)		
			
			for contact in groupContacts:
				contactID = str(contact[0])
				contactName = contact[1]
				
				contactNode = QtGui.QTreeWidgetItem(groupNode)
				contactNode.setText(1, contactID)
				contactNode.setText(0, contactName)
				self.ui.contactsTree.addTopLevelItem(contactNode)					

	def onContactClick(self):
	
		self.ui.imageLabel.hide()

		# opening database
		self.tempdb = sqlite3.connect(self.filename)
		self.tempdb.row_factory = sqlite3.Row
		self.tempcur = self.tempdb.cursor() 
		
		currentSelectedElement = self.ui.contactsTree.currentItem()
		if (currentSelectedElement): pass
		else: return
		
		contactID = currentSelectedElement.text(1)
		if (len(contactID) == 0):
			return # it's a group

		contactID = int(contactID)
		self.ui.contactsTable.clear()
		self.ui.contactsTable.setHorizontalHeaderLabels(["Key", "Value"])
		self.ui.contactsTable.setRowCount(100)
		
		# Main contact data
		
		query = "SELECT First, Last, Organization, Middle, Department, Note, Birthday, JobTitle, Nickname FROM ABPerson WHERE ROWID = \"%i\""%contactID
		self.tempcur.execute(query)
		user = self.tempcur.fetchall()[0]

		records = [
			["First name", user['First']],
			["Last name", user['Last']],
			["Organization", user['Organization']],
			["Middle name", user['Middle']],
			["Department", user['Department']],
			["Note", user['Note']],
			["Birthday", user['Birthday']],
			["Job Title", user['JobTitle']],
			["Nickname", user['Nickname']],
		]
		
		row = 0
		
		for record in records:
			key = record[0]
			value = record[1]
			
			if (value != None):
				newItem = QtGui.QTableWidgetItem(key)
				self.ui.contactsTable.setItem(row, 0, newItem)	
				newItem = QtGui.QTableWidgetItem(value)
				self.ui.contactsTable.setItem(row, 1, newItem)	

				row = row + 1
		
		# multivalues
		query = "SELECT property, label, value, UID FROM ABMultiValue WHERE record_id = \"%s\""%contactID
		self.tempcur.execute(query)
		multivalues = self.tempcur.fetchall()
		
		# acquire multivalue labels
		query = "SELECT value FROM ABMultiValueLabel"
		self.tempcur.execute(query)
		multivaluelabels = self.tempcur.fetchall()

		# acquire multivalue labels keys
		query = "SELECT value FROM ABMultiValueEntryKey"
		self.tempcur.execute(query)
		multivalueentrykeys = self.tempcur.fetchall()		
		
		# print multivalues
		for multivalue in multivalues:
			
			# decode multivalue type
			if (multivalue[0] == 3):	
				property = "Phone number"
			elif (multivalue[0] == 4):
				property = "EMail address"
			elif (multivalue[0] == 5):
				property = "Multivalue"
			elif (multivalue[0] == 22):
				property = "URL"
			else: 
				property = "Unknown (%s)"%multivalue[0]
			
			# decode multivalue label
			label = ""
			if (multivalue[1] != None):
				label = multivaluelabels[int(multivalue[1]) - 1][0]
				label = lstrip(label, "_!<$")
				label = rstrip(label, "_!>$")
			
			value = multivalue[2]
			
			# if multivalue is multipart (an address)...
			if (multivalue[0] == 5):
				multivalueid = multivalue[3]
				query = "SELECT KEY, value FROM ABMultiValueEntry WHERE parent_id = \"%i\" ORDER BY key"%multivalueid
				self.tempcur.execute(query)
				parts = self.tempcur.fetchall()

				newItem = QtGui.QTableWidgetItem("Address (%s):"%label)
				self.ui.contactsTable.setItem(row, 0, newItem)	
		
				multipartText = ""
		
				for part in parts:
				
					partkey = part[0]
					partvalue = part[1]
					label = multivalueentrykeys[int(partkey) - 1][0]
					
					multipartText += "%s: %s\n"%(label, partvalue)	
				
				newItem = QtGui.QTableWidgetItem(multipartText)
				self.ui.contactsTable.setItem(row, 1, newItem)				
				
				row = row + 1					
				
			else:
			
				newItem = QtGui.QTableWidgetItem("%s (%s)"%(property, label))
				self.ui.contactsTable.setItem(row, 0, newItem)	
				newItem = QtGui.QTableWidgetItem(value)
				self.ui.contactsTable.setItem(row, 1, newItem)	
				row = row + 1	

		self.ui.contactsTable.setRowCount(row)
		self.ui.contactsTable.resizeColumnsToContents()		
		self.ui.contactsTable.resizeRowsToContents()
		self.ui.contactsTable.horizontalHeader().setStretchLastSection(True)	
		
		self.tempdb.close()
		
		# retrieve image (if available)
		if (self.thumbsfilename != None):
		
			# opening database
			self.tempdb = sqlite3.connect(self.thumbsfilename)
			self.tempdb.row_factory = sqlite3.Row
			self.tempcur = self.tempdb.cursor() 	

			query = "SELECT data FROM ABThumbnailImage WHERE record_id = %s"%contactID
			self.tempcur.execute(query)
			result = self.tempcur.fetchall()
			if (len(result) > 0):
			
				imagedata = str(result[0][0])
				im = QtCore.QByteArray(imagedata)	
				qimg = QtGui.QImage.fromData(im)
				qpixmap = QtGui.QPixmap.fromImage(qimg).scaled(100, 100, QtCore.Qt.KeepAspectRatio)
				
				self.ui.imageLabel.setPixmap(qpixmap)
				self.ui.imageLabel.show()

			# closing database
			self.tempdb.close()


	def contactsList(self):
	
		peopleData = []
		additionalResources = []

		# opening database
		self.tempdb = sqlite3.connect(self.filename)
		self.tempdb.row_factory = sqlite3.Row
		self.tempcur = self.tempdb.cursor() 
		
		# acquire multivalue labels (just once)
		query = "SELECT value FROM ABMultiValueLabel"
		self.tempcur.execute(query)
		multivaluelabels = self.tempcur.fetchall()

		# acquire multivalue labels keys (just once)
		query = "SELECT value FROM ABMultiValueEntryKey"
		self.tempcur.execute(query)
		multivalueentrykeys = self.tempcur.fetchall()			
		
		# retrieve people list
		query = 'SELECT * FROM ABPerson;'
		self.tempcur.execute(query)
		people = self.tempcur.fetchall()

		for person in people:
			
			personData = []
			
			contactID = person['ROWID']

			# complete name
			if (person['First'] != None):
				name = person['First']
			if (person['Last'] != None):
				name = name + " " + person['Last']
			if (person['First'] == None and person['Last'] == None):
				name = person['Organization']	
			if (name == None):
				name = "<None>"
			personData.append(["Full name", self.clearHtml(name)])
			
					
			records = [
				["First name", person['First']],
				["Last name", person['Last']],
				["Organization", person['Organization']],
				["Middle name", person['Middle']],
				["Department", person['Department']],
				["Note", person['Note']],
				["Birthday", person['Birthday']],
				["Job Title", person['JobTitle']],
				["Nickname", person['Nickname']],
			]
			
			for record in records: 				
				if (record[1] != None):
					personData.append([self.clearHtml(record[0]), self.clearHtml(record[1])])
					
			# multivalues
			query = "SELECT property, label, value, UID FROM ABMultiValue WHERE record_id = \"%s\""%contactID
			self.tempcur.execute(query)
			multivalues = self.tempcur.fetchall()
		
			# print multivalues
			for multivalue in multivalues:
				
				# decode multivalue type
				if (multivalue[0] == 3):	
					property = "Phone number"
				elif (multivalue[0] == 4):
					property = "EMail address"
				elif (multivalue[0] == 5):
					property = "Multivalue"
				elif (multivalue[0] == 22):
					property = "URL"
				else: 
					property = "Unknown (%s)"%multivalue[0]
				
				# decode multivalue label
				label = ""
				if (multivalue[1] != None):
					label = multivaluelabels[int(multivalue[1]) - 1][0]
					label = lstrip(label, "_!<$")
					label = rstrip(label, "_!>$")
				
				value = multivalue[2]
				
				# if multivalue is multipart (an address)...
				if (multivalue[0] == 5):
					multivalueid = multivalue[3]
					query = "SELECT KEY, value FROM ABMultiValueEntry WHERE parent_id = \"%i\" ORDER BY key"%multivalueid
					self.tempcur.execute(query)
					parts = self.tempcur.fetchall()
					
					multipartKey = "Address (%s):"%self.clearHtml(label)
			
					multipartValue = ""
					for part in parts:
					
						partkey = part[0]
						partValue = part[1]
						label = multivalueentrykeys[int(partkey) - 1][0]
						
						multipartValue += "%s: %s<br>"%(self.clearHtml(label), self.clearHtml(partValue))

					personData.append([multipartKey, multipartValue])
					
				else:				
					personData.append(["%s (%s)"%(self.clearHtml(property), self.clearHtml(label)), self.clearHtml(value)])
			

			# retrieve image (if available)
			if (self.thumbsfilename != None):
			
				# opening database
				self.tempThumbDb = sqlite3.connect(self.thumbsfilename)
				self.tempThumbDb.row_factory = sqlite3.Row
				self.tempThumbCur = self.tempThumbDb.cursor() 	

				query = "SELECT data FROM ABThumbnailImage WHERE record_id = %s"%contactID
				self.tempThumbCur.execute(query)
				result = self.tempThumbCur.fetchall()
				if (len(result) > 0):
				
					imageData = str(result[0][0])
					tempFile = plugins_utils.pluginTempFile()

					writer = open(tempFile, 'wb')
					writer.write(imageData)
					writer.close()
					
					additionalResources.append([tempFile, "%i.bmp"%contactID])
					
					personData.append(["Photo", '<img src="%s" \>'%os.path.join("$IPBA2RESOURCESPATH$", "%i.bmp"%contactID)])
					
				# closing database
				self.tempThumbDb.close()

		
			peopleData.append(personData)
		
		self.tempdb.close()
		
		return (peopleData, additionalResources)
			
		



def main(cursor, path):
	try:
		return AddressBookWidget(cursor, path)
	except:
		plugins_utils.error("Unable to open Contacts file in backup archive.")
		return None
		
def report(cursor, path):
	widget = AddressBookWidget(cursor, path, True)
	peopleData, files = widget.contactsList()
	
	ritorno = ""
	ritorno += "<h1>Address Book</h1>"
	
	ritorno += "<ul>"
	
	for person in peopleData:
		ritorno += "<li>"
		ritorno += person[0][1]
		ritorno += "<table>"
		for element in person[1:]:
			ritorno += "<tr><td>%s</td><td>%s</td></tr>"%(element[0], element[1])
		ritorno += "</table>"
		ritorno += "</li>"
	
	ritorno += "</ul>"
	
	return (ritorno, files)