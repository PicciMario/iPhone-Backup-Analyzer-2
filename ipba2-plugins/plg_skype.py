from PySide import QtCore, QtGui
from skype_ui import Ui_Skype

import os, sqlite3, sys
from datetime import datetime
from string import *

PLUGIN_NAME = "Skype Browser"
import plugins_utils

# retrieve modules from ipba root directory
import plistutils

############################################################################################################################

class Chat_message:

	#init
	def __init__(self, record, m_id, timestamp, author, from_dispname, mess, status, mess_type, chatname, dialog_partner,edited_timestamp):
				
		#message record
		self.record = str(record)
		
		#message id
		self.m_id = str(m_id)
		
		#Parse various date times.
		self.timestamp = self.parse_date(timestamp)
		
		#author and displayname
		self.author = author
		self.from_dispname = self.parse_text(from_dispname)
		
		self.mess = self.parse_text(mess)           
		self.status = self.check_status(status)          
				   
		self.mess_type = self.check_type(mess_type)  
		self.chatname = chatname  
		
		self.edited_timestamp = self.parse_date(edited_timestamp)
			 
		self.dialog_partner = self.parse_text(dialog_partner)
			
	def __str__(self):
		mess_to_string = self.mess	
		return mess_to_string

	#Parse text method
	def parse_text(self, value):    
		#try:
		#	value = str(value)
		#	if value == "None":
		#		value = " "
		#except UnicodeEncodeError:
		#	value = value.encode("utf-8")
		if (value == None): 
			return ""
		return value      
		
	def check_status(self, value):
		if value == 4:
			value = "Read"
		if value == 3:
			value = "Not Read"
		elif value == 2:
			value = "Sent"	
		elif value == 1:
			value = "Not Delivered Yet"	
		return value	
	
	def check_type(self, value):
		if value == 61:
			value = "POSTED_TEXT"
		if value == 50:
			value = "Auth_Request"
		if value == 51:
			value = "Auth_Granted"		
		if value == 53:
			value = "Auth_Denied"		
		if value == 30:
			value = "STARTED_LIVESESSION"		
		if value == 39:
			value = "ENDED_LIVESESSION"		
		if value == 68:
			value = "FILE TRANSFER"		
		return value

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

class Call:
	
	#init
	def __init__(self, record, c_id, begin_timestamp, duration, call_type, call_type_img, host_identity, remote_host, remote_host_displayname, status ):
				
		#call record
		self.record = str(record)
		#call id
		self.c_id = str(c_id)
		
		#Parse various date times.
		self.begin_timestamp = self.parse_date(begin_timestamp)
		
		#Duration
		#convert the call duration from seconds to minutes:seconds.
		self.duration = self.convert_seconds(duration)
	
		self.call_type_img = call_type_img
		self.call_type = self.check_call_type(call_type)
		self.host_identity = self.check_host(host_identity, remote_host)		
		self.remote_host = remote_host  
		self.status = self.check_status(status)  
		self.remote_host_displayname = remote_host_displayname     
			
					   
	def check_status(self, value):
		if value == 6:
			value = "Accepted"
		elif value == 8:
			value = "Rejected at Destination"
		elif value == 13 or value == 7:
			value = "Cancelled at Origin"
		else:
			value = "Other status - Not recognized "			
		return value
		
	def __str__(self):
		id_to_string = self.c_id
		host_identity_to_string = self.host_identity
		remote_host_to_string = self.remote_host

		return id_to_string, host_identity_to_string, remote_host_to_string
				
		#I'm getting the local host name from the guid field, like:  
		#jessicaleone2-nicodemo.j.gawronski-1347550499-1 where one of the names is the host name.
		#remove the remote_host identity, any digit and all the "-":           
	
	def check_host(self, host_to_convert, remote_host): 
		
		if host_to_convert != None:
			split1, split2, split3, split4 = host_to_convert.split("-")
			if split1 == remote_host:
				host_to_convert = split2
			else:
				host_to_convert = split1	
			
		else:
			host_to_convert = " "
		return host_to_convert

	def check_call_type(self, value):
		if value == 1:
			value = "Incoming"
			self.call_type_img = "../../resources/incoming.png"
		elif value == 2:
			value = "Outgoing"
			self.call_type_img = "../../resources/outgoing.png"
		else:
			value = "Unknown (%i)"%value
		return value	

	#convert the call duration from seconds to minutes:seconds.
	def convert_seconds(self, value):
		try:
			seconds = value%60
			minutes = value/60
			hours = 0
			if minutes >= 60:
				hours = minutes/60
				minutes = minutes%60
			if minutes < 10:
				minutes = "0"+str(minutes)
			if hours < 10:
				hours = "0"+str(hours)	
			if seconds < 10:
				seconds = "0"+str(seconds)	
					
			value = str(hours)+ ":" +str(minutes)+ ":" +str(seconds)
		
		except TypeError:
			value = " "
			
		return value	

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

class Transfer:
	
	#init
	def __init__(self, record, t_id, partner_handle, partner_dispname, filename, file_type, filepath,
		filesize, bytestransferred, starttime, endtime, status):
			
			#call record
			self.record = str(record)
			
			#call id
			self.t_id = str(t_id)
			
			#Parse various date times.
			self.starttime = self.parse_date(starttime)
			self.endtime = self.parse_date(endtime)	
	
			self.partner_handle = partner_handle		
			self.partner_dispname = partner_dispname
			self.filename = filename            
			self.file_type = self.check_type(file_type)          
			self.filepath = filepath  
			self.filesize = filesize  
			self.bytestransferred = bytestransferred  
			self.status = self.check_status(status)  

	def check_type(self, value):
		if value == 1:
			value = "Incoming File Transfer"
		elif value == 2:
			value = "Outgoing File Transfer"
		return value	

	def check_status(self, value):
		if value == 8:
			value = "Completed"
		elif value == 7:
			value = "Aborted From Destination"	
		elif value == 10:
			value = "Aborted From Origin"	
					
		return value	

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

class Group_chat:
	
	#init
	def __init__(self, record, c_id, name, participants, posters, active_members, friendlyname, timestamp,
	  last_change):

			#message record
			self.record = str(record)
			#message id
			self.c_id = str(c_id)

			self.name = name
			self.participants = participants
			self.posters = posters
			self.active_members = active_members
			self.friendlyname = self.parse_text(friendlyname)
			
			#Parse various date times.
			self.timestamp = self.parse_date(timestamp)
			self.last_change = self.parse_date(last_change)

	#Parse text method
	def parse_text(self, value):    
		try:
			value = str(value)
			if value == "None":
				value = " "
		except UnicodeEncodeError:
			value = value.encode("utf-8")
		return value
		
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

class Voicemail:
	
	#init
	def __init__(self, record, v_id, partner_handle, partner_dispname, subject, timestamp, duration, allowed_duration,
	  size, path, failures, convo_id):

		#message record
		self.record = str(record)
		#message id
		self.v_id = str(v_id)
		
		self.partner_handle = partner_handle
		self.partner_dispname = partner_dispname
		self.subject = subject
		self.duration = duration
		self.allowed_duration = allowed_duration
		self.size = self.parse_text(size)
		self.path = path
		self.failures = failures
		self.convo_id = convo_id
		
		#Parse various date times.
		self.timestamp = self.parse_date(timestamp)
			
			
	#Parse text method
	def parse_text(self, value):    
		try:
			value = str(value)
			if value == "None":
				value = " "
		except UnicodeEncodeError:
			value = value.encode("utf-8")
		return value      

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

class Account:
	
	# init
	def __init__(self, record, a_id, skypename, displayname, fullname, birthday, gender, img, city, province,
	 country, lastonline_timestamp,home_phone, office_phone, mobile_phone, emails, homepage, about, creation_date, mood_text, lastused_timestamp, avatar, avatar_timestamp):

		#record
		self.record = str(record)
		#contact id
		self.a_id = str(a_id)
		
		#Skypename
		self.skypename = str(skypename)
		
		#Displayname
		self.displayname = self.parse_text(displayname)
		#Fullname
		self.fullname = self.parse_text(fullname)
		
		#Birthday
		self.birthday = str(birthday)
		#print self.birthday
		if self.birthday == "None" or self.birthday == "0":
			self.birthday = " "
		elif self.birthday.isdigit() is True:
			#print self.birthday
			year = self.birthday[0:4]
			month = self.birthday[4:6]
			day = self.birthday[6:8]
			self.birthday = day + "-" + month + "-" + year
		
		#Parse various date times.
		self.lastonline_timestamp = self.parse_date(lastonline_timestamp)
		self.lastused_timestamp = self.parse_date(lastused_timestamp)
		self.avatar_timestamp = self.parse_date(avatar_timestamp)
		 
		#Use a different parser because the date is not like 1202680620 but like 20044677,
		#both equal to 2008-02-10 21:57:00
		self.creation_date = self.parse_creation(creation_date)
			
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
		
		#output_avatar = this_report_complete_tree+self.a_id+"_avatar.jpg"
		#if self.avatar != None:
		#	with open(output_avatar, "wb") as o:
		#		o.write(self.avatar[1:])    
		#		o.close()
		#		self.avatar = "avatar/"+self.a_id+"_avatar.jpg"
		#else:
		#	self.avatar = " "        
		
		
	def __str__(self):
		id_to_string = self.c_id
		skypename_to_string = self.skypename
		mood_to_string = self.mood_text

		return id_to_string, skypename_to_string, mood_to_string
	
	
	#Parse text method
	def parse_text(self, value):    
		try:
			value = str(value)
			if "<script" in value:
				value = "<textarea>"+value+"</textarea>"
			if value == "None":
				value = " "
		except UnicodeEncodeError:
			value = value.encode("utf-8")
		return value

	
	def parse_creation (self,value):
		try:
			value = value*60
			value = datetime.fromtimestamp(value)
			value = datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
			value = value.strftime('%d-%m-%Y %H:%M:%S')
		except TypeError:
			value = " "
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
			img = " "
			gender = " "

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

		# TEST ONLY
		#self.filename = "D:\Forensics\iPhone forensics\iPhone-Backup-Analyzer-2\main.db"

		# check if files exist
		if (not os.path.isfile(self.filename)):
			raise Exception("Skype database not found: \"%s\""%self.filename)
			
		if (daemon == False):
			self.populateUI()

	#-------------------------------------------------------------------------------

	def populateUI(self):
		
		# UI settings for contacts tab
		QtCore.QObject.connect(self.ui.contactsTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onContactsTreeClick)
		self.ui.contactsTree.setColumnHidden(0,True)
		self.ui.imageLabel.hide()

		# UI settings for calls tab
		QtCore.QObject.connect(self.ui.callsTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onCallsTreeClick)
		self.ui.callsTree.setColumnHidden(0,True)
		self.ui.callsTree.setColumnWidth(1,130)
		
		# UI settings for messages tab
		QtCore.QObject.connect(self.ui.messagesTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onMessagesTreeClick)
		self.ui.messagesTree.setColumnHidden(0,True)
		self.ui.messagesTree.setColumnWidth(1,130)	

		# UI settings for transfers tab
		QtCore.QObject.connect(self.ui.transfersTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onTransfersTreeClick)
		self.ui.transfersTree.setColumnHidden(0,True)
		self.ui.transfersTree.setColumnWidth(1,130)	

		# UI settings for group chats tab
		QtCore.QObject.connect(self.ui.groupChatsTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onGroupChatsTreeClick)
		self.ui.groupChatsTree.setColumnHidden(0,True)
		self.ui.groupChatsTree.setColumnWidth(1,130)

		# UI settings for accounts tab
		QtCore.QObject.connect(self.ui.accountsTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onAccountsTreeClick)
		self.ui.accountsTree.setColumnHidden(0,True)
		self.ui.accountsTree.setColumnWidth(1,130)	
		self.ui.accountLabel.hide()
	
		# populating contacts tab
		self.extractedContacts = self.get_contacts()
		index = 0
		for contact in self.extractedContacts:
			node = QtGui.QTreeWidgetItem(None)
			node.setText(0, str(index))
			node.setText(1, contact.skypename)
			self.ui.contactsTree.addTopLevelItem(node)
			index += 1

		# populating calls tab
		self.extractedCalls = self.get_calls()
		index = 0
		for call in self.extractedCalls:
			node = QtGui.QTreeWidgetItem(None)
			node.setText(0, str(index))
			node.setText(1, call.begin_timestamp)
			node.setText(2, call.remote_host)
			node.setText(3, call.status)
			self.ui.callsTree.addTopLevelItem(node)
			index += 1
		
		# populating messages tab
		self.extractedMessages = self.get_chat_messages()
		index = 0
		for message in self.extractedMessages:
			node = QtGui.QTreeWidgetItem(None)
			node.setText(0, str(index))
			node.setText(1, message.timestamp)
			node.setText(2, message.author)
			node.setText(3, message.dialog_partner)
			self.ui.messagesTree.addTopLevelItem(node)
			index += 1

		# populating transfers tab
		self.extractedTransfers = self.get_transfers()
		index = 0
		for transfer in self.extractedTransfers:
			node = QtGui.QTreeWidgetItem(None)
			node.setText(0, str(index))
			node.setText(1, transfer.starttime)
			node.setText(2, transfer.partner_handle)
			node.setText(3, transfer.filename)
			node.setText(4, transfer.status)
			self.ui.transfersTree.addTopLevelItem(node)
			index += 1
	
		# populating group chats tab
		self.extractedGroupChats = self.get_group_chats()
		index = 0
		for groupChat in self.extractedGroupChats:
			node = QtGui.QTreeWidgetItem(None)
			node.setText(0, str(index))
			node.setText(1, groupChat.timestamp)
			node.setText(2, groupChat.participants)
			self.ui.groupChatsTree.addTopLevelItem(node)
			index += 1

		# populating voicemails tab
		self.extractedVoicemails = self.get_voicemails()
		index = 0
		for voicemail in self.extractedVoicemails:
			node = QtGui.QTreeWidgetItem(None)
			node.setText(0, str(index))
			node.setText(1, voicemail.timestamp)
			node.setText(2, voicemail.partner_dispname)
			node.setText(3, voicemail.subject)
			self.ui.voicemailsTree.addTopLevelItem(node)
			index += 1

		# populating accounts tab
		self.extractedAccounts = self.get_accounts()
		index = 0
		for account in self.extractedAccounts:
			node = QtGui.QTreeWidgetItem(None)
			node.setText(0, str(index))
			node.setText(1, account.skypename)
			node.setText(2, account.fullname)
			self.ui.accountsTree.addTopLevelItem(node)
			index += 1
			
	#-------------------------------------------------------------------------------
	
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

	#-------------------------------------------------------------------------------

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
		
		connection.close()
		
		return contact_list
	
	#-------------------------------------------------------------------------------

	def onCallsTreeClick(self):
	
		currentSelectedElement = self.ui.callsTree.currentItem()
		if (currentSelectedElement): pass
		else: return		
		
		callID = int(currentSelectedElement.text(0))
		call = self.extractedCalls[callID]
		
		elements = [
			["Timestamp", call.begin_timestamp],
			["Duration", str(call.duration)],
			["Status", call.status],
			["Call type", str(call.call_type)],
			["Host identity", call.host_identity],
			["Remote host", call.remote_host],
			["Remote host name", call.remote_host_displayname],
		]
		
		self.ui.callsTable.clear()
		self.ui.callsTable.setHorizontalHeaderLabels(["Field", "Value"])
		self.ui.callsTable.setRowCount(100)
		self.ui.callsTable.setColumnCount(2)
		
		row = 0
		for element in elements:
			if (len(element[1].strip()) > 0):
				newItem = QtGui.QTableWidgetItem(element[0])
				self.ui.callsTable.setItem(row, 0, newItem)	
				newItem = QtGui.QTableWidgetItem(element[1])
				self.ui.callsTable.setItem(row, 1, newItem)
				row = row + 1	
				
		self.ui.callsTable.setRowCount(row)
		self.ui.callsTable.resizeColumnsToContents()		
		self.ui.callsTable.horizontalHeader().setStretchLastSection(True)
		self.ui.callsTable.resizeRowsToContents()
		
	#-------------------------------------------------------------------------------

	def get_calls(self):
		
		call_list = []
		
		# open database
		connection = sqlite3.connect(self.filename)
		connection.row_factory = sqlite3.Row

		cursor = connection.cursor()
		   
		#Get the name of each table in the database.
		cursor.execute('SELECT * FROM CallMembers')
		
		calls = cursor.fetchall()
		
		for call in calls:
			
			# ------------------------------------------------------- #
			#  Skype main.db file *** CallMembers TABLE  #
			# ------------------------------------------------------- #
			# call[0] --> id					call[1] --> is_permanent 		call[2] --> identity
			# call[3] --> dispname				call[4] --> languages 			call[5] --> call_duration
			# call[6] --> price_per_minute		call[7] --> price_precision 	call[8] --> price_currency
			# call[9] --> payment_category		call[10] --> type 				call[11] --> status
			# call[12] --> failurereason		call[13] --> sounderror_code 	call[14] --> soundlevel
			# call[15] --> pstn_statustext		call[16] --> pstn_feedback 		call[17] --> forward_targets
			# call[18] --> forwarded_by			call[19] --> debuginfo 			call[20] --> videostatus
			# call[21] --> target_identity		call[22] --> mike_status 		call[23] --> is_read_only
			# call[24] --> quality_status		call[25] --> call_name 			call[26] --> transfer_status
			# call[27] --> transfer_active		call[28] --> transferred_by 	call[29] --> transferred_to
			# call[30] --> guid					call[31] --> next_redial_time 	call[32] --> nrof_redials_done
			# call[33] --> nrof_redials_left	call[34] --> transfer_topic 	call[35] --> real_identity
			# call[36] --> start_timestamp		call[37] --> is_conference 		call[38] --> quality_problems
			# call[39] --> identity_type		call[40] --> country 			call[41] --> creation_timestamp
			# call[42] --> stats_xml			call[43] --> is_premium_video_sponsor 		call[44] --> is_multiparty_video_capable
			# call[45] --> recovery_in_progress	call[46] --> nonse_word 		call[47] --> pk_status                       
			
			record = len(call_list)
				
			curr_call = Call(
				record, 
				call["id"], 
				call["creation_timestamp"], 
				call["call_duration"], 
				call["type"],
				None, 
				call["guid"],
				call["identity"], 
				call["dispname"], 
				call["status"]
			)
			call_list.append(curr_call)
		
		connection.close()
	
		return call_list

	#-------------------------------------------------------------------------------
	
	def onMessagesTreeClick(self):
	
		currentSelectedElement = self.ui.messagesTree.currentItem()
		if (currentSelectedElement): pass
		else: return		
		
		messageID = int(currentSelectedElement.text(0))
		message = self.extractedMessages[messageID]
		
		elements = [
			["Timestamp", message.timestamp],
			["Author", message.author],
			["From (display name)", message.from_dispname],
			["Message", message.mess],
			["Status", message.status if message.status != None else "None" ],
			["Message type", str(message.mess_type)],
			["Chat name", message.chatname],
			["Edited timestamp", message.edited_timestamp],
			["Dialog partner", message.dialog_partner],
		]
		
		self.ui.messagesTable.clear()
		self.ui.messagesTable.setHorizontalHeaderLabels(["Field", "Value"])
		self.ui.messagesTable.setRowCount(100)
		self.ui.messagesTable.setColumnCount(2)
		
		row = 0
		for element in elements:
			if (len(element[1].strip()) > 0):
				newItem = QtGui.QTableWidgetItem(element[0])
				self.ui.messagesTable.setItem(row, 0, newItem)	
				newItem = QtGui.QTableWidgetItem(element[1])
				self.ui.messagesTable.setItem(row, 1, newItem)
				row = row + 1	
				
		self.ui.messagesTable.setRowCount(row)
		self.ui.messagesTable.resizeColumnsToContents()		
		self.ui.messagesTable.horizontalHeader().setStretchLastSection(True)
		self.ui.messagesTable.resizeRowsToContents()
		
	#-------------------------------------------------------------------------------

	def get_chat_messages(self):
		
		chat_messages_list = []
		
		# open database
		connection = sqlite3.connect(self.filename)
		connection.row_factory = sqlite3.Row

		cursor = connection.cursor()
		   
		cursor.execute('SELECT * FROM Messages ORDER BY timestamp')
		
		messages = cursor.fetchall()
		
		for message in messages:
			
			# ------------------------------------------------------- #
			#  Skype main.db file *** Messages TABLE  #
			# ------------------------------------------------------- #
			# message[0] --> id					message[1] --> is_permanent message[2] --> convo_id
			# message[3] --> chatname			message[4] --> author 		message[5] --> from_dispname
			# message[6] --> author_was_live	message[7] --> guid 		message[8] --> dialog_partner
			# message[9] --> timestamp			message[10] --> type 		message[11] --> sending_status
			# message[12] -->consumption_status	message[13] --> edited_by 	message[14] --> edited_timestamp
			# message[15] --> param_key			message[16] --> param_value message[17] --> body_xml
			# message[18] --> identities		message[19] --> reason 		message[20] --> leavereason
			# message[21] --> participant_count	message[22] --> error_code 	message[23] --> chatmsg_type
			# message[24] --> chatmsg_status	message[25] --> body_is_rawxml 		message[26] --> oldoptions
			# message[27] --> newoptions		message[28] --> newrole 	message[29] --> pk_id
			# message[30] --> crc				message[31] --> remote_id 	message[32] --> call_guid

			record = len(chat_messages_list)
				
			curr_mess = Chat_message(
				record, 
				message["id"], 
				message["timestamp"], 
				message["author"], 
				message["from_dispname"], 
				message["body_xml"], 
				message["chatmsg_status"], 
				message["type"],
				message["chatname"],
				message["dialog_partner"], 
				message["edited_timestamp"] 
			)
			chat_messages_list.append(curr_mess)
		
		return chat_messages_list
	#-------------------------------------------------------------------------------
	
	def onTransfersTreeClick(self):
	
		currentSelectedElement = self.ui.transfersTree.currentItem()
		if (currentSelectedElement): pass
		else: return		
		
		transferID = int(currentSelectedElement.text(0))
		transfer = self.extractedTransfers[transferID]
		
		elements = [
			["Start time", transfer.starttime],
			["End time", transfer.endtime],
			["Partner handle", transfer.partner_handle],
			["Partner display name", transfer.partner_dispname],
			["Filename", transfer.filename],
			["File type", transfer.file_type],
			["File path", transfer.filepath],
			["File size", transfer.filesize],
			["Bytes transferred", transfer.bytestransferred],
			["Status", transfer.status],
		]
		
		self.ui.transfersTable.clear()
		self.ui.transfersTable.setHorizontalHeaderLabels(["Field", "Value"])
		self.ui.transfersTable.setRowCount(100)
		self.ui.transfersTable.setColumnCount(2)
		
		row = 0
		for element in elements:
			if (element[1] == None):
				element[1] = "None"
			if (len(element[1].strip()) > 0):
				newItem = QtGui.QTableWidgetItem(element[0])
				self.ui.transfersTable.setItem(row, 0, newItem)	
				newItem = QtGui.QTableWidgetItem(element[1])
				self.ui.transfersTable.setItem(row, 1, newItem)
				row = row + 1	
				
		self.ui.transfersTable.setRowCount(row)
		self.ui.transfersTable.resizeColumnsToContents()		
		self.ui.transfersTable.horizontalHeader().setStretchLastSection(True)
		self.ui.transfersTable.resizeRowsToContents()
		
	#-------------------------------------------------------------------------------
		
	def get_transfers(self):
		
		transfers_list = []
		
		# open database
		connection = sqlite3.connect(self.filename)
		connection.row_factory = sqlite3.Row

		cursor = connection.cursor()
		   
		cursor.execute('SELECT * FROM Transfers')
		
		transfers = cursor.fetchall()
		
		for transfer in transfers:
			
			# ------------------------------------------------------- #
			#  Skype main.db file *** Transfers TABLE  #
			# ------------------------------------------------------- #
			# transfer[0] --> id				transfer[1] --> is_permanent 		transfer[2] --> type
			# transfer[3] --> partner_handle	transfer[4] --> partner_dispname 	transfer[5] --> status
			# transfer[6] --> failurereason		transfer[7] --> starttime 			transfer[8] --> finishtime
			# transfer[9] --> filepath			transfer[10] --> filename 			transfer[11] --> filesize
			# transfer[12] --> bytestransferred	transfer[13] --> bytespersecond 	transfer[14] --> chatmsg_guid
			# transfer[15] --> chatmsg_index	transfer[16] --> convo_id 			transfer[17] --> pk_id
			# transfer[18] --> nodeid			transfer[19] --> last_activity 		transfer[20] --> flags
			# transfer[21] --> old_status		transfer[22] --> old_filepath 		transfer[23] --> accepttime
			
			record = len(transfers_list)
						
			curr_trans = Transfer(
				record, 
				transfer["id"], 
				transfer["partner_handle"], 
				transfer["partner_dispname"], 
				transfer["filename"], 
				transfer["type"], 
				transfer["filepath"],
				transfer["filesize"], 
				transfer["bytestransferred"], 
				transfer["starttime"], 
				transfer["finishtime"], 
				transfer["status"]
			)
			transfers_list.append(curr_trans)
		
		return transfers_list

	#-------------------------------------------------------------------------------
		
	def onGroupChatsTreeClick(self):
	
		currentSelectedElement = self.ui.groupChatsTree.currentItem()
		if (currentSelectedElement): pass
		else: return		
		
		groupChatID = int(currentSelectedElement.text(0))
		groupChat = self.extractedGroupChats[groupChatID]
		
		elements = [
			["Name", groupChat.name],
			["Participants", groupChat.participants],
			["Posters", groupChat.posters],
			["Active members", groupChat.active_members],
			["Friendly name", groupChat.friendlyname],
			["Timestamp", groupChat.timestamp],
			["Last change", groupChat.last_change],
		]
		
		self.ui.groupChatsTable.clear()
		self.ui.groupChatsTable.setHorizontalHeaderLabels(["Field", "Value"])
		self.ui.groupChatsTable.setRowCount(100)
		self.ui.groupChatsTable.setColumnCount(2)
		
		row = 0
		for element in elements:
			if (len(element[1].strip()) > 0):
				newItem = QtGui.QTableWidgetItem(element[0])
				self.ui.groupChatsTable.setItem(row, 0, newItem)	
				newItem = QtGui.QTableWidgetItem(element[1])
				self.ui.groupChatsTable.setItem(row, 1, newItem)
				row = row + 1	
				
		self.ui.groupChatsTable.setRowCount(row)
		self.ui.groupChatsTable.resizeColumnsToContents()		
		self.ui.groupChatsTable.horizontalHeader().setStretchLastSection(True)
		self.ui.groupChatsTable.resizeRowsToContents()
		
	#-------------------------------------------------------------------------------

	def get_group_chats(self):
		
		group_chat_list = []
		
		# open database
		connection = sqlite3.connect(self.filename)
		connection.row_factory = sqlite3.Row

		cursor = connection.cursor()
		   
		cursor.execute('SELECT * FROM Chats WHERE type = 4')
		
		chats = cursor.fetchall()
		
		for chat in chats:
			
			# ------------------------------------------------------- #
			#  Skype main.db file *** Chats TABLE  #
			# ------------------------------------------------------- #
			# chat[0] --> id						chat[1] --> is_permanent 		chat[2] --> name
			# chat[3] --> options					chat[4] --> friendlyname 		chat[5] --> description
			# chat[6] --> timestamp					chat[7] --> activity_timestamp	chat[8] --> dialog_partner
			# chat[9] --> adder						chat[10] --> type 				chat[11] --> mystatus
			# chat[12] --> myrole					chat[13] --> posters 			chat[14] --> participants
			# chat[15] --> applicants				chat[16] --> banned_users 		chat[17] --> name_text
			# chat[18] --> topic					chat[19] --> topic_xml 			chat[20] --> guidelines
			# chat[21] --> picture					chat[22] --> alertstring 		chat[23] --> is_bookmarked
			# chat[24] --> passwordhint				chat[25] --> unconsumed_suppressed_msg 		chat[26] --> unconsumed_normal_msg
			# chat[27] --> unconsumed_elevated_msg	chat[28] --> unconsumed_msg_voice chat[29] --> activemembers
			# chat[30] --> state_data				chat[31] --> lifesigns 			chat[32] --> last_change
			# chat[33] --> first_unread_message		chat[34] --> pk_type 			chat[35] --> dbpath

			record = len(group_chat_list)
			
			curr_chat = Group_chat(
				record, 
				chat["id"], 
				chat["name"], 
				chat["participants"], 
				chat["posters"], 
				chat["activemembers"], 
				chat["friendlyname"], 
				chat["timestamp"],
				chat["last_change"]
			)
			  
			group_chat_list.append(curr_chat)
			
		return group_chat_list

	#-------------------------------------------------------------------------------
		
	def onVoicemailsTreeClick(self):
	
		currentSelectedElement = self.ui.voicemailsTree.currentItem()
		if (currentSelectedElement): pass
		else: return		
		
		voicemailID = int(currentSelectedElement.text(0))
		voicemail = self.extractedVoicemails[voicemailID]
		
		elements = [
			["Partner handle", voicemail.partner_handle],
			["Partner display name", voicemail.partner_dispname],
			["Timestamp", voicemail.timestamp],
			["Subject", voicemail.subject],
			["Duration", voicemail.duration],
			["Allowed duration", voicemail.allowed_duration],
			["Size", voicemail.size],
			["Path", voicemail.path],
			["Failures", voicemail.failures],
			["Convo ID", voicemail.convo_id],
		]
		
		self.ui.voicemailsTable.clear()
		self.ui.voicemailsTable.setHorizontalHeaderLabels(["Field", "Value"])
		self.ui.voicemailsTable.setRowCount(100)
		self.ui.voicemailsTable.setColumnCount(2)
		
		row = 0
		for element in elements:
			if (len(element[1].strip()) > 0):
				newItem = QtGui.QTableWidgetItem(element[0])
				self.ui.voicemailsTable.setItem(row, 0, newItem)	
				newItem = QtGui.QTableWidgetItem(element[1])
				self.ui.voicemailsTable.setItem(row, 1, newItem)
				row = row + 1	
				
		self.ui.voicemailsTable.setRowCount(row)
		self.ui.voicemailsTable.resizeColumnsToContents()		
		self.ui.voicemailsTable.horizontalHeader().setStretchLastSection(True)
		self.ui.voicemailsTable.resizeRowsToContents()

	#-------------------------------------------------------------------------------

	def get_voicemails(self):
		
		voicemails_list = []
		
		# open database
		connection = sqlite3.connect(self.filename)
		connection.row_factory = sqlite3.Row

		cursor = connection.cursor()
		   
		cursor.execute('SELECT * FROM Voicemails')
		
		voicemails = cursor.fetchall()
		
		for voice in voicemails:
			
			# ------------------------------------------------------- #
			#  Skype main.db file *** Voicemails TABLE  #
			# ------------------------------------------------------- #
			# voice[0] --> id				voice[1] --> is_permanent 		voice[2] --> type
			# voice[3] --> partner_handle	voice[4] --> partner_dispname 	voice[5] --> status
			# voice[6] --> failurereason	voice[7] --> subject 			voice[8] --> timestamp
			# voice[9] --> duration			voice[10] --> allowed_duration 	voice[11] --> playback_progress
			# voice[12] --> convo_id		voice[13] --> chatmsg_guid 		voice[14] --> notification_id
			# voice[15] --> flags			voice[16] --> size 				voice[17] --> path
			# voice[18] --> failures		voice[19] --> vflags 			voice[20] --> xmsg

			record = len(voicemails_list)
			
			curr_voice = Voicemail(
				record, 
				voice["id"], 
				voice["partner_handle"], 
				voice["partner_dispname"], 
				voice["subject"], 
				voice["timestamp"], 
				voice["duration"], 
				voice["allowed_duration"],
				voice["size"], 
				voice["path"], 
				voice["failures"], 
				voice["convo_id"]	
			)
			
			voicemails_list.append(curr_voice)
		
		return voicemails_list
	
	#-------------------------------------------------------------------------------

	def onAccountsTreeClick(self):
	
		currentSelectedElement = self.ui.accountsTree.currentItem()
		if (currentSelectedElement): pass
		else: return		
		
		accountID = int(currentSelectedElement.text(0))
		account = self.extractedAccounts[accountID]
		
		elements = [
			["Skype name", account.skypename],
			["Display name", account.displayname],
			["Full name", account.fullname],
			["Birthday", account.birthday],
			["Last time online", account.lastonline_timestamp],
			["Last time used", account.lastused_timestamp],
			["Avatar timestamp", account.avatar_timestamp],
			["Creation date", account.creation_date],
			["Gender", account.gender],
			["City", account.city],
			["Province", account.province],
			["Country", account.country],
			["Home phone", account.home_phone],
			["Office phone", account.office_phone],
			["Mobile phone", account.mobile_phone],
			["Emails", account.emails],
			["Homepage", account.homepage],
			["About", account.about],
			["Mood text", account.mood_text],
		]
		
		self.ui.accountsTable.clear()
		self.ui.accountsTable.setHorizontalHeaderLabels(["Field", "Value"])
		self.ui.accountsTable.setRowCount(100)
		self.ui.accountsTable.setColumnCount(2)
		
		row = 0
		for element in elements:
			if (len(element[1].strip()) > 0):
				newItem = QtGui.QTableWidgetItem(element[0])
				self.ui.accountsTable.setItem(row, 0, newItem)	
				newItem = QtGui.QTableWidgetItem(element[1])
				self.ui.accountsTable.setItem(row, 1, newItem)
				row = row + 1	
				
		self.ui.accountsTable.setRowCount(row)
		self.ui.accountsTable.resizeColumnsToContents()		
		self.ui.accountsTable.horizontalHeader().setStretchLastSection(True)
		self.ui.accountsTable.resizeRowsToContents()
		
		# Image data
		imagedata = account.avatar
		if (imagedata != None):
			im = QtCore.QByteArray(imagedata)	
			qimg = QtGui.QImage.fromData(im)
			qpixmap = QtGui.QPixmap.fromImage(qimg).scaled(120, 120, QtCore.Qt.KeepAspectRatio)
			
			self.ui.accountLabel.setPixmap(qpixmap)
			self.ui.accountLabel.show()
		else:
			self.ui.accountLabel.hide()
	
	#-------------------------------------------------------------------------------
	
	def get_accounts(self):    
	
		account_list = []
		
		# open database
		connection = sqlite3.connect(self.filename)
		connection.row_factory = sqlite3.Row

		cursor = connection.cursor()
		   
		#Get the name of each table in the database.
		cursor.execute('SELECT * FROM Accounts')
		
		accounts = cursor.fetchall()
		
		for account in accounts:
			
			# ------------------------------------------------------- #
			#  Skype main.db file *** Accounts TABLE  #
			# ------------------------------------------------------- #
			# accounts[0] --> id						accounts[1] --> is_permanent 				accounts[2] --> status
			# accounts[3] --> pwdchangestatus			accounts[4] --> logoutreason 				accounts[5] --> commitstatus
			# accounts[6] --> suggested_skypename		accounts[7] --> skypeout_balance_currency 	accounts[8] --> skypeout_balance
			# accounts[9] --> skypeout_precision		accounts[10] --> skypein_numbers 			accounts[11] --> subscriptions
			# accounts[12] --> cblsyncstatus			accounts[13] --> offline_callforward 		accounts[14] --> chat_policy
			# accounts[15] --> skype_call_policy		accounts[16] --> pstn_call_policy 			accounts[17] --> avatar_policy
			# accounts[18] --> buddycount_policy		accounts[19] --> timezone_policy 			accounts[20] --> webpresence_policy
			# accounts[21] --> phonenumbers_policy		accounts[22] --> voicemail_policy 			accounts[23] --> authrequest_policy
			# accounts[24] --> ad_policy				accounts[25] --> partner_optedout 			accounts[26] --> service_provider_info
			# accounts[27] --> registration_timestamp	accounts[28] --> nr_of_other_instances 		accounts[29] --> partner_channel_status
			# accounts[30] --> flamingo_xmpp_status		accounts[31] --> federated_presence_policy 	accounts[32] --> owner_under_legal_age
			# accounts[33] --> type						accounts[34] --> skypename 					accounts[35] --> pstnnumber
			# accounts[36] --> fullname					accounts[37] --> birthday 					accounts[38] --> gender
			# accounts[39] --> languages				accounts[40] --> country 					accounts[41] --> province
			# accounts[42] --> city						accounts[43] --> phone_home 				accounts[44] --> phone_office
			# accounts[45] --> phone_mobile				accounts[46] --> emails 					accounts[47] --> homepage
			# accounts[48] --> about					accounts[49] --> profile_timestamp 			accounts[50] --> received_authrequest
			# accounts[51] --> displayname				accounts[52] --> refreshing 				accounts[53] --> given_authlevel
			# accounts[54] --> aliases					accounts[55] --> authreq_timestamp 			accounts[56] --> mood_text
			# accounts[57] --> timezone					accounts[58] --> nrof_authed_buddies 		accounts[59] --> ipcountry
			# accounts[60] --> given_displayname		accounts[61] --> availability 				accounts[62] --> lastonline_timestamp
			# accounts[63] --> capabilities				accounts[64] --> avatar_image 				accounts[65] --> assigned_speeddial
			# accounts[66] --> lastused_timestamp		accounts[67] --> authrequest_count 			accounts[68] --> assigned_comment
			# accounts[69] --> alertstring				accounts[70] --> avatar_timestamp 			accounts[71] --> mood_timestamp
			# accounts[72] --> rich_mood_text			accounts[73] --> synced_email 				accounts[74] --> set_availability
			# accounts[75] --> options_change_future	accounts[76] --> cbl_profile_blob 			accounts[77] --> authorized_time
			# accounts[78] --> sent_authrequest			accounts[79] --> sent_authrequest_time 		accounts[80] --> sent_authrequest_serial
			# accounts[81] --> buddyblob				accounts[82] --> cbl_future 				accounts[83] --> node_capabilities
			# accounts[84] --> node_capabilities_and	accounts[85] --> revoked_auth 				accounts[86] --> added_in_shared_group
			# accounts[87] --> in_shared_group			accounts[88] --> authreq_history 			accounts[89] --> profile_attachments
			# accounts[90] --> stack_version			accounts[91] --> offline_authreq_id 		accounts[92] --> verified_email
			# accounts[93] --> verified_company			accounts[94] --> liveid_membername 			accounts[95] --> roaming_history_enabled
						
			record = len(account_list)
			
			curr_account = Account(
				record, 
				account["id"], 
				account["skypename"], 
				account["displayname"], 
				account["fullname"], 
				account["birthday"], 
				account["gender"], 
				None, 
				account["city"], 
				account["province"], 
				account["country"], 
				account["lastonline_timestamp"], 
				account["phone_home"], 
				account["phone_office"], 
				account["phone_mobile"], 
				account["emails"], 
				account["homepage"], 
				account["about"], 
				account["registration_timestamp"],  
				account["mood_text"], 
				account["lastused_timestamp"], 
				account["avatar_image"], 
				account["avatar_timestamp"],
			)        
			
			account_list.append(curr_account)
		
		connection.close()
		
		return account_list	

############################################################################################################################

def main(cursor, path):
	return SkypeWidget(cursor, path)