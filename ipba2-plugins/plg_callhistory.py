from PySide import QtCore, QtGui
from callhistory_ui import Ui_CallHistory

import os, sqlite3
from datetime import datetime

PLUGIN_NAME = "Call History"
import plugins_utils

class CallHistoryWidget(QtGui.QWidget):
	
	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_CallHistory()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		self.filename = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename="call_history.db", domaintype="WirelessDomain"))
		self.addressbookfilename = os.path.join(self.backup_path, plugins_utils.realFileName(cursor, filename="AddressBook.sqlitedb", domaintype="HomeDomain"))

		# check if files exist
		if (not os.path.isfile(self.filename)):
			raise Exception("Call History database not found: \"%s\""%self.filename)
		if (not os.path.isfile(self.addressbookfilename)):
			self.addressbookfilename = None
		
		if (daemon == False):
			self.populateUI()
		

	def populateUI(self):
		
		# populating keys tree
		keys = self.getKeys()
		
		self.ui.keysTable.setRowCount(len(keys))
		
		row = 0
		for element in keys:
			text = element[0]
			value = element[1]
		
			newItem = QtGui.QTableWidgetItem(text)
			self.ui.keysTable.setItem(row, 0, newItem)	
			newItem = QtGui.QTableWidgetItem(value)
			self.ui.keysTable.setItem(row, 1, newItem)

			row = row + 1

		self.ui.keysTable.resizeColumnsToContents()		
		self.ui.keysTable.resizeRowsToContents()
		self.ui.keysTable.horizontalHeader().setStretchLastSection(True)
	
		# reading calls from database
		calls = self.getCalls()
		
		self.ui.callsTable.setRowCount(len(calls))
		
		row = 0
		for call in calls:
		
			rowid = call[0]
			address = call[1]
			date = call[2]
			duration = call[3]
			flags = call[4]
			id = call[5]
			name = call[6]
			country_code = call[7]
			addrName = call[8]
			
			newItem = QtGui.QTableWidgetItem(str(rowid))
			self.ui.callsTable.setItem(row, 0, newItem)				
			newItem = QtGui.QTableWidgetItem(address)
			self.ui.callsTable.setItem(row, 1, newItem)	
			newItem = QtGui.QTableWidgetItem(str(date))
			self.ui.callsTable.setItem(row, 2, newItem)	
			newItem = QtGui.QTableWidgetItem(duration)
			self.ui.callsTable.setItem(row, 3, newItem)	
			newItem = QtGui.QTableWidgetItem(flags)
			self.ui.callsTable.setItem(row, 4, newItem)	
			newItem = QtGui.QTableWidgetItem(addrName)
			self.ui.callsTable.setItem(row, 5, newItem)				
			row = row + 1
	
		self.ui.callsTable.resizeColumnsToContents()		
		self.ui.callsTable.resizeRowsToContents()
		self.ui.callsTable.horizontalHeader().setStretchLastSection(True)		


	def getKeys(self):

		# opening database
		self.tempdb = sqlite3.connect(self.filename)
		self.tempcur = self.tempdb.cursor()
	
		keys = []

		# description, field name, has to be time formatted?
		keysList = [
			["Call history limit", "call_history_limit", False],
			["Last call duration", "timer_last", True],
			["Incoming calls duration", "timer_incoming", True],
			["Outgoing calls duration", "timer_outgoing", True],
			["Total call duration (from reset)", "timer_all", True],
			["Total lifetime call duration", "timer_lifetime", True],
		]
		
		for element in keysList:
			text = element[0]
			key = element[1].encode('utf-8')
			timeFormatted = element[2]
			
			value = self.readKey(key)
			if (timeFormatted):
				value = self.formatTime(value)
		
			keys.append([text, value])
		
		# closing database
		self.tempdb.close()
		
		return keys
		
		
	def getCalls(self):
	
		# opening database
		self.tempdb = sqlite3.connect(self.filename)
		self.tempcur = self.tempdb.cursor()
	
		callsToReturn = []
	
		# reading calls from database
		query = "SELECT ROWID, address, date, duration, flags, id, name, country_code FROM call ORDER BY date"
		self.tempcur.execute(query)
		calls = self.tempcur.fetchall()
		
		for call in calls:
			rowid = call[0]
			address = call[1]
			date = datetime.fromtimestamp(int(call[2]))
			duration = self.formatTime(call[3])
			
			flagval = call[4]
			if (flagval == 5): flags = "Outgoing"
			elif (flagval == 4): flags = "Incoming"
			else: flags = "Cancelled"
			
			id = call[5]
			name = call[6].encode('utf-8')
			country_code = call[7]	
			
			addrName = ""
	
			# check if can find name in address book
			if (self.addressbookfilename != None and id != -1):

				# opening database
				self.tempaddrdb = sqlite3.connect(self.addressbookfilename)
				self.tempaddrcur = self.tempaddrdb.cursor()
					
				query = "SELECT First, Last, Organization FROM ABPerson WHERE ROWID = ?;"
				self.tempaddrcur.execute(query, (id,))
				addrQuery = self.tempaddrcur.fetchall()			
				
				if (len(addrQuery) > 0):
					
					addrFirst = addrQuery[0][0]
					addrLast = addrQuery[0][1]
					addrOrganization = addrQuery[0][2]
				
					if (addrFirst != None):
						addrName = addrFirst + " "
					if (addrLast != None):
						addrName = addrName + addrLast
					if (addrFirst == None and addrLast == None):
						addrName = addrOrganization				
				
				# closing database
				self.tempaddrdb.close()		

			callsToReturn.append([rowid, address, date, duration, flags, id, name, country_code, addrName])

		# closing database
		self.tempdb.close()				
			
		return callsToReturn


	def readKey(self, key):
		query = "SELECT value FROM _SqliteDatabaseProperties WHERE key = \"%s\""%key
		self.tempcur.execute(query)
		data = self.tempcur.fetchall()
		if (len(data) > 0):
			value = data[0][0]
		else:
			value = 0
		return value	
		
	def formatTime(self, seconds):
		durationtot = int(seconds)
		durationmin = int(durationtot / 60)
		durationhh = int(durationmin / 60)
		durationmin = durationmin - (durationhh * 60)
		durationsec = durationtot - (durationmin * 60) - (durationhh * 3600)
		duration = "%i:%.2i:%.2i"%(durationhh, durationmin, durationsec)	
		return duration	

	def setTitle(self, title):
		self.setWindowTitle(title)


def main(cursor, path):
	return CallHistoryWidget(cursor, path)
	
def report(cursor, path):
	
	returnString = ""

	callHistory = CallHistoryWidget(cursor, path, daemon = True)
	keys = callHistory.getKeys()
	calls = callHistory.getCalls()
	del callHistory
	
	returnString += "<h1>Call History</h1>\n"
	
	returnString += "<h2>Summary</h2>\n"
	
	returnString += "<table><tr><th>Key</th><th>Value</th></tr>\n"
	for key in keys:
		returnString += "<tr><td>%s</td><td>%s</td></tr>\n"%(key[0], key[1])
	returnString += "</table>\n"
	
	returnString += "<h2>Calls list</h2>\n"
	
	returnString += "<table><tr><th>rowid</th><th>address</th><th>date</th><th>duration</th><th>flags</th><th>id</th><th>name</th><th>country code</th><th>Name (from address book)</th></tr>\n"
	for call in calls:
		returnString += "<tr>"
		returnString += "<td>%s</td>"%call[0]
		returnString += "<td>%s</td>"%call[1]
		returnString += "<td>%s</td>"%call[2]
		returnString += "<td>%s</td>"%call[3]
		returnString += "<td>%s</td>"%call[4]
		returnString += "<td>%s</td>"%call[5]
		returnString += "<td>%s</td>"%call[6]
		returnString += "<td>%s</td>"%call[7]
		returnString += "<td>%s</td>"%call[8]
		returnString += "</tr>\n"
	
	returnString += "</table>"
	
	return returnString
	