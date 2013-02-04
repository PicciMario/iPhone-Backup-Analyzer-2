from PySide import QtCore, QtGui
from general_ui import Ui_General

import os, sqlite3, sys
from datetime import datetime

PLUGIN_NAME = "General Phone Info"
import plugins_utils

# retrieve modules from ipba root directory
import plistutils

class GeneralWidget(QtGui.QWidget):
	
	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_General()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		self.infoFileName = os.path.join(self.backup_path, "Info.plist")
		self.manifestFileName = os.path.join(self.backup_path, "Manifest.plist")
		self.statusFileName = os.path.join(self.backup_path, "Status.plist")
		
		if (daemon == False):
			self.populateUI()
		
	def retrieveInfoKeys(self):
		infoProperties = []
		infoPlist = plistutils.readPlist(self.infoFileName)
		
		keysToBlockInInfoPlist = [
			"iBooks Data 2",
			"iTunes Settings",
			"iTunes Files"
		]
		
		for key in infoPlist.keys():
			if (key not in keysToBlockInInfoPlist):
				infoProperties.append([key, infoPlist[key]])
		
		return infoProperties
	
	def retrieveManifestKeys(self):
		manifestProperties = []
		manifestPlist = plistutils.readPlist(self.manifestFileName)
		
		manifestProperties.append(["Backup Computer Name", manifestPlist['Lockdown']['com.apple.iTunes.backup']['LastBackupComputerName'] ])
		manifestProperties.append(["Encrypted Backup", manifestPlist['IsEncrypted'] ])
		manifestProperties.append(["Passcode Set", manifestPlist['WasPasscodeSet'] ])
		
		return manifestProperties

	def retrieveApps(self):
		appsList = []
		manifestPlist = plistutils.readPlist(self.manifestFileName)
		
		for key in manifestPlist['Applications'].keys():
			appsList.append([key, manifestPlist['Applications'][key]['CFBundleVersion'] ])
		
		return appsList
	
	def retrieveStatusKeys(self):
		statusProperties = []
		statusPlist = plistutils.readPlist(self.statusFileName)
		
		for key in statusPlist.keys():
			statusProperties.append([key, statusPlist[key]])
		
		return statusProperties
		
		
	def populateUI(self):	

		# phone info records (from info.plist)
		
		phoneInfo = QtGui.QTreeWidgetItem(None)
		phoneInfo.setText(0, "Phone info")
		self.ui.infoTree.addTopLevelItem(phoneInfo)

		for element in self.retrieveInfoKeys():
			key = str(element[0])
			value = str(element[1])
			
			newElement = QtGui.QTreeWidgetItem(phoneInfo)
			newElement.setText(0, key)
			newElement.setText(1, value)
			self.ui.infoTree.addTopLevelItem(newElement)

		for element in self.retrieveManifestKeys():
			key = str(element[0])
			value = str(element[1])
			
			newElement = QtGui.QTreeWidgetItem(phoneInfo)
			newElement.setText(0, key)
			newElement.setText(1, value)
			self.ui.infoTree.addTopLevelItem(newElement)

		# backup status (from status.plist)
		
		backupStatus = QtGui.QTreeWidgetItem(None)
		backupStatus.setText(0, "Backup Status")
		self.ui.infoTree.addTopLevelItem(backupStatus)

		for element in self.retrieveStatusKeys():
			key = str(element[0])
			value = str(element[1])
			
			newElement = QtGui.QTreeWidgetItem(backupStatus)
			newElement.setText(0, key)
			newElement.setText(1, value)
			self.ui.infoTree.addTopLevelItem(newElement)		

		# apps list (from manifest.plist)
		
		appsList = QtGui.QTreeWidgetItem(None)
		appsList.setText(0, "Apps list")
		self.ui.infoTree.addTopLevelItem(appsList)
		
		for element in self.retrieveApps():
			name = str(element[0])
			version = str(element[1])
		
			newElement = QtGui.QTreeWidgetItem(appsList)
			newElement.setText(0, name)
			newElement.setText(1, version)
			self.ui.infoTree.addTopLevelItem(newElement)			
		
		self.ui.infoTree.resizeColumnToContents(0)
		self.ui.infoTree.resizeColumnToContents(1)


def main(cursor, path):
	return GeneralWidget(cursor, path)

def report(cursor, path):
	widget = GeneralWidget(cursor, path, True)
	
	phoneInfoKeys = widget.retrieveInfoKeys()
	phoneManifestKeys = widget.retrieveManifestKeys()
	backupKeys = widget.retrieveStatusKeys()
	appsList = widget.retrieveApps()
	
	del widget
	
	ritorno = ""
	ritorno += "<h1>Phone General Information</h1>"
	
	ritorno += "<h2>Phone Info</h2>"
	ritorno += "<table>"
	for element in phoneInfoKeys:
		ritorno += "<tr><td>%s</td><td>%s</td></tr>"%(str(element[0]), str(element[1]))
	for element in phoneManifestKeys:
		ritorno += "<tr><td>%s</td><td>%s</td></tr>"%(str(element[0]), str(element[1]))
	ritorno += "</table>"
	
	ritorno += "<h2>Backup Status</h2>"
	ritorno += "<table>"
	for element in backupKeys:
		ritorno += "<tr><td>%s</td><td>%s</td></tr>"%(str(element[0]), str(element[1]))
	ritorno += "</table>"

	ritorno += "<h2>Apps List</h2>"
	ritorno += "<table>"
	for element in appsList:
		ritorno += "<tr><td>%s</td><td>%s</td></tr>"%(str(element[0]), str(element[1]))
	ritorno += "</table>"
	
	return ritorno