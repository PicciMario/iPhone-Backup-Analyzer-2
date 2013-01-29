from PySide import QtCore, QtGui
from callhistory_ui import Ui_CallHistory

import os, sqlite3
from datetime import datetime

PLUGIN_NAME = "Call History"
import plugins_utils

class CallHistoryWidget(QtGui.QWidget):
	
	def __init__(self, cursor, path):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_CallHistory()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		self.filename = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename="call_history.db", domaintype="WirelessDomain"))

		# opening database
		self.tempdb = sqlite3.connect(self.filename)
		self.tempcur = self.tempdb.cursor() 
		
		# populating keys tree
		
		# description, field name, has to be time formatted?
		keysList = [
			["Call history limit", "call_history_limit", False],
			["Last call duration", "timer_last", True],
			["Incoming calls duration", "timer_incoming", True],
			["Outgoing calls duration", "timer_outgoing", True],
			["Total call duration (from reset)", "timer_all", True],
			["Total lifetime call duration", "timer_lifetime", True],
		]
		
		self.ui.keysTable.setRowCount(len(keysList))
		
		row = 0
		for element in keysList:
			text = element[0]
			key = element[1]
			timeFormatted = element[2]
			
			value = self.readKey(key)
			if (timeFormatted):
				value = self.formatTime(value)
		
			newItem = QtGui.QTableWidgetItem(text)
			self.ui.keysTable.setItem(row, 0, newItem)	
			newItem = QtGui.QTableWidgetItem(value)
			self.ui.keysTable.setItem(row, 1, newItem)

			row = row + 1

		self.ui.keysTable.resizeColumnsToContents()		
		self.ui.keysTable.resizeRowsToContents()
	
		# reading calls from database
		query = "SELECT ROWID, address, date, duration, flags, id, name, country_code FROM call ORDER BY date"
		self.tempcur.execute(query)
		calls = self.tempcur.fetchall()
		
		# closing database
		self.tempdb.close()
		
		self.ui.callsTable.setRowCount(len(calls))
		
		row = 0
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
			name = call[6]
			country_code = call[7]
			
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
			
			row = row + 1
	
		self.ui.callsTable.resizeColumnsToContents()		
		self.ui.callsTable.resizeRowsToContents()		

	def readKey(self, key):
		query = "SELECT value FROM _SqliteDatabaseProperties WHERE key = \"%s\""%key
		self.tempcur.execute(query)
		data = self.tempcur.fetchall()
		if (len(data) > 0):
			value = data[0][0]
		else:
			value = 0
		return value

	def addKey(self, text, value):
		newNode = QtGui.QTreeWidgetItem(None)
		newNode.setText(0, text)
		newNode.setText(1, value)
		self.ui.keysTree.addTopLevelItem(newNode)	
		
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