from PySide import QtCore, QtGui
from skype_ui import Ui_Skype

import os, sqlite3, sys
from datetime import datetime
from string import *

PLUGIN_NAME = "Skype Browser"
import plugins_utils

# retrieve modules from ipba root directory
import plistutils

class Contact:

	# init
	def __init__(self, record, c_id, skypename, displayname, birthday, lastonline_timestamp, is_permanent,isblocked, isauthorized, availability, final_status, gender, img, city, province, country, home_phone, office_phone, mobile_phone, emails, homepage, about,
	profile_timestamp, mood_text, lastused_timestamp, avatar_timestamp, avatar):
		
		global this_report_complete_tree
		#record
		self.record = str(record)
		
		#contact id
		self.c_id = str(c_id)
		
		#Skypename
		self.skypename = str(skypename)
		
		#Displayname
		self.displayname = self.parse_text(displayname)
		
		#Birthday
		self.birthday = str(birthday)
		if self.birthday == "None":
			self.birthday = " "
		elif self.birthday.isdigit() is True:
			#print self.birthday
			year = self.birthday[0:4]
			month = self.birthday[4:6]
			day = self.birthday[6:8]
			self.birthday = day+"-"+month+"-"+year
		
		#Parse various date times.
		self.lastonline_timestamp = self.parse_date(lastonline_timestamp)
		self.lastused_timestamp = self.parse_date(lastused_timestamp)
		self.avatar_timestamp = self.parse_date(avatar_timestamp)
		self.profile_timestamp = self.parse_date(profile_timestamp)

		#Check contact status
		self.is_permanent = is_permanent
		self.isblocked = isblocked
		self.isauthorized = isauthorized
		self.availability = availability    
		self.final_status = self.check_status(is_permanent, isblocked, isauthorized, availability)
		
		#Gender
		self.img, self.gender = self.check_gender(gender)		
		
		#city text
		self.city = self.parse_text(city)
		
		#province text
		self.province = self.parse_text(province)
		
		#country text
		self.country = self.parse_text(country)
		
		#home_phone text
		self.home_phone = self.parse_text(home_phone)
		
		#office_phone text
		self.office_phone = self.parse_text(office_phone)
		
		#mobile_phone text
		self.mobile_phone = self.parse_text(mobile_phone)
		
		#emails text
		self.emails = self.parse_text(emails)
		
		#homepage text
		self.homepage = self.parse_text(homepage)
		
		#about text        
		self.about = self.parse_text(about)        
		
		#mood text
		self.mood_text = self.parse_text(mood_text)
		
		#avatar image
		#Save the avatar image to a img/avatar/ folder.
		#This image is named by (contact_id)_avatar.jpg
		#Change the value of self.avatar to path+(id)_avatar.jpg
		
		if (avatar != None):
			self.avatar = avatar[1:]
		else:
			self.avatar = None
	
		#output_avatar = this_report_complete_tree+self.c_id+"_avatar.jpg"
		#if self.avatar != None:
		#	with open(output_avatar, "wb") as o:
		#		
		#		o.write(self.avatar[1:])    
		#		o.close()
		#		self.avatar = "avatar/"+self.c_id+"_avatar.jpg"
		#else:
		#	self.avatar = " "        		
		
	def __str__(self):
		id_to_string = self.c_id
		skypename_to_string = self.skypename
		mood_to_string = self.mood_text

		return id_to_string, skypename_to_string, mood_to_string        
		
	def check_status(self, is_permanent, isblocked, isauthorized, availability):
		stat = []
		stat = [is_permanent, isblocked, isauthorized, availability]
		result = ""
		#print self.skypename, stat
		if stat[0] == 1 and stat[1] == None and stat[2] == 1 and stat[3] != 8:
			result = "Usual Contact"
		elif stat[0] == 1 and stat[1] == None and stat[2] == 1 and stat[3] == 8:
			result = "In your list but never seen online"
		elif stat[0] == 1 and stat[1] == None and stat[2] == None:
			result = "Deleted"
		elif stat[0] == 1 and stat[1] == 1:
			result = "Blocked"
		elif stat[0] == 0:
			result = "Not in your contact list, probably seen in a group chat"
		#if stat[3] == 8:
			#print self.skypename, stat, result  
		#print result							
		return result
		
	#Parse text method
	def parse_text(self, value):    
		try:
			value = str(value)
			#if "<script" in value:
					#value = "<textarea>"+value+"</textarea>"
			if value == "None":
				value = ""
		except UnicodeEncodeError:
			value = value.encode("utf-8")
		return value

	def check_gender(self, gender):
		img = gender
	
		if gender == 1:
			img = "../../resources/male.png"
			gender = "Male"
		elif gender == 2:
			img = "../../resources/female.png"
			gender = "Female"
		else:
			img = ""
			gender = ""	
			
		return img, gender	     

	#Parse date like 1357674582 into date like this Day-Month-Year Hour:Minute:Second		
	def parse_date(self, value):
		if value != 0:
			try:
				value = datetime.utcfromtimestamp(value)
				value = datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
				value = value.strftime('%d-%m-%Y %H:%M:%S')
			except TypeError:
				value = " "
		else:
			value = " "        
		return value

############################################################################################################################

class SkypeWidget(QtGui.QWidget):
	
	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_Skype()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		self.filename = os.path.join(self.backup_path, plugins_utils.realFileName(cursor, filename="main.db", domaintype="AppDomain", domain="com.skype.skype"))

		# check if files exist
		if (not os.path.isfile(self.filename)):
			raise Exception("Skype database not found: \"%s\""%self.filename)
			
		if (daemon == False):
			self.populateUI()


	def populateUI(self):
		
		# UI settings for contacts tab
		QtCore.QObject.connect(self.ui.contactsTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onContactsTreeClick)
		self.ui.contactsTree.setColumnHidden(0,True)
		self.ui.imageLabel.hide()
	
		# populating contacts tab
		self.extractedContacts = self.get_contacts()
		index = 0
		for contact in self.extractedContacts:
			node = QtGui.QTreeWidgetItem(None)
			node.setText(0, str(index))
			node.setText(1, contact.skypename)
			self.ui.contactsTree.addTopLevelItem(node)
			index += 1
	
	def onContactsTreeClick(self):
		currentSelectedElement = self.ui.contactsTree.currentItem()
		if (currentSelectedElement): pass
		else: return		
		
		contactID = int(currentSelectedElement.text(0))
		contact = self.extractedContacts[contactID]
		
		elements = [
			["Skype Name", contact.skypename],
			["Display name", contact.displayname],
			["Birthday", contact.birthday],
			["Last seen online", contact.lastonline_timestamp],
			["Last used", contact.lastused_timestamp],
			["Avatar timestamp", contact.avatar_timestamp],
			["Profile timestamp", contact.profile_timestamp],
			["Status", contact.final_status],
			["Gender", contact.gender],
			["City", contact.city],
			["Province", contact.province],
			["Country", contact.country],
			["Home phone", contact.home_phone],
			["Office phone", contact.office_phone],
			["Mobile phone", contact.mobile_phone],
			["Email", contact.emails],
			["Homepage", contact.homepage],
			["About", contact.about],
			["Mood text", contact.mood_text],
		]
		
		self.ui.contactsTable.clear()
		self.ui.contactsTable.setHorizontalHeaderLabels(["Field", "Value"])
		self.ui.contactsTable.setRowCount(100)
		self.ui.contactsTable.setColumnCount(2)
		
		row = 0
		for element in elements:
			if (len(element[1].strip()) > 0):
				newItem = QtGui.QTableWidgetItem(element[0])
				self.ui.contactsTable.setItem(row, 0, newItem)	
				newItem = QtGui.QTableWidgetItem(element[1])
				self.ui.contactsTable.setItem(row, 1, newItem)
				row = row + 1	
				
		self.ui.contactsTable.setRowCount(row)
		self.ui.contactsTable.resizeColumnsToContents()		
		self.ui.contactsTable.resizeRowsToContents()
		self.ui.contactsTable.horizontalHeader().setStretchLastSection(True)
		
		# Image data
		imagedata = contact.avatar
		if (imagedata != None):
			im = QtCore.QByteArray(imagedata)	
			qimg = QtGui.QImage.fromData(im)
			qpixmap = QtGui.QPixmap.fromImage(qimg).scaled(120, 120, QtCore.Qt.KeepAspectRatio)
			
			self.ui.imageLabel.setPixmap(qpixmap)
			self.ui.imageLabel.show()
		else:
			self.ui.imageLabel.hide()

	def get_contacts(self):

		contact_list = []
		
		# open database
		connection = sqlite3.connect(self.filename)
		connection.row_factory = sqlite3.Row

		cursor = connection.cursor()
		   
		#Get the name of each table in the database.
		cursor.execute('SELECT * FROM Contacts')
		
		contacts = cursor.fetchall()
		
		for contact in contacts:
			
			# ------------------------------------------------------- #
			#  Skype main.db file *** Contacts TABLE  #
			# ------------------------------------------------------- #
			# contacts[0] --> id				 	contacts[1] --> is_permanent 		contacts[2] --> type
			# contacts[3] --> skypename			 	contacts[4] --> pstnnumber 		contacts[5] --> aliases
			# contacts[6] --> fullname			 	contacts[7] --> birthday 		contacts[8] --> gender
			# contacts[9] --> languages			 	contacts[10] --> country 		contacts[11] --> province
			# contacts[12] --> city				 	contacts[13] --> phone_home 		contacts[14] --> phone_office
			# contacts[15] --> phone_mobile		 	contacts[16] --> emails 		contacts[17] --> homepage
			# contacts[18] --> about			 	contacts[19] --> avatar_image 		contacts[20] --> mood_text
			# contacts[21] --> rich_mood_text	 	contacts[22] --> timezone 		contacts[23] --> capabilities
			# contacts[24] --> profile_timestamp 	contacts[25] --> nrof_authed_buddies 		contacts[26] --> ipcountry
			# contacts[27] --> avatar_timestamp	 	contacts[28] --> mood_timestamp 		contacts[29] --> received_authrequest
			# contacts[30] --> authreq_timestamp 	contacts[31] --> lastonline_timestamp 		contacts[32] --> availability
			# contacts[33] --> displayname		 	contacts[34] --> refreshing 		contacts[35] --> given_authlevel
			# contacts[36] --> given_displayname 	contacts[37] --> assigned_speeddial 		contacts[38] --> assigned_comment
			# contacts[39] --> alertstring		 	contacts[40] --> lastused_timestamp 		contacts[41] --> authrequest_count
			# contacts[42] --> assigned_phone1	 	contacts[43] --> assigned_phone1_label 		contacts[44] --> assigned_phone2
			# contacts[45] --> assigned_phone2_labelcontacts[46] --> assigned_phone3 	contacts[47] --> assigned_phone3_label
			# contacts[48] --> buddystatus			contacts[49] --> isauthorized 		contacts[50] --> popularity_ord
			# contacts[51] --> isblocked			contacts[52] --> authorization_certificate 		contacts[53] --> certificate_send_count
			# contacts[54] --> account_modification_serial_nr		contacts[55] --> saved_directory_blob 		contacts[56] --> nr_of_buddies
			# contacts[57] --> server_synced		contacts[58] --> contactlist_track 		contacts[59] --> last_used_networktime
			# contacts[60] --> authorized_time		contacts[61] --> sent_authrequest 		contacts[62] --> sent_authrequest_time
			# contacts[63] --> sent_authrequest_serial		contacts[64] --> buddyblob 		contacts[65] --> cbl_future
			# contacts[66] --> node_capabilities	contacts[67] --> revoked_auth 		contacts[68] --> added_in_shared_group
			# contacts[69] --> in_shared_group		contacts[70] --> authreq_history 		contacts[71] --> profile_attachments
			# contacts[72] --> stack_version		contacts[73] --> offline_authreq_id 		contacts[74] --> node_capabilities_and
			# contacts[75] --> authreq_crc			contacts[76] --> authreq_src 		contacts[77] --> pop_score
			# contacts[78] --> authreq_nodeinfo		contacts[79] --> main_phone 		contacts[80] --> unified_servants
			# contacts[81] --> phone_home_normalized		contacts[82] --> phone_office_normalized 		contacts[83] --> phone_mobile_normalized
			# contacts[84] --> sent_authrequest_initmethod		contacts[85] --> authreq_initmethod contacts[86] --> verified_email
			# contacts[87] --> verified_company		contacts[88] --> sent_authrequest_extrasbitmask 		contacts[89] --> extprop_tags		
			record = len(contact_list)
			
						
			curr_contact = Contact(
				record, 
				contact["id"], 
				contact["skypename"], 
				contact["displayname"], 
				contact["birthday"], 
				contact["lastonline_timestamp"], 
				contact["is_permanent"], 
				contact["isblocked"], 
				contact["isauthorized"], 
				contact["availability"], 
				None,
				contact["gender"], 
				None, 
				contact["city"], 
				contact["province"], 
				contact["country"], 
				contact["phone_home"], 
				contact["phone_office"], 
				contact["phone_mobile"], 
				contact["emails"], 
				contact["homepage"], 
				contact["about"], 
				contact["profile_timestamp"], 
				contact["mood_text"], 
				contact["lastused_timestamp"], 
				contact["avatar_timestamp"], 
				contact["avatar_image"] 
			)
			contact_list.append(curr_contact)
		
		return contact_list





def main(cursor, path):
	return SkypeWidget(cursor, path)