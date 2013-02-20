from PySide import QtCore, QtGui
from knownnetworks_ui import Ui_KnownNetworks

import os, sqlite3, plistlib
from datetime import datetime

PLUGIN_NAME = "Known WiFi Networks"
import plugins_utils

# retrieve modules from ipba root directory
import plistutils

class KnownNetworksWidget(QtGui.QWidget):
	
	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_KnownNetworks()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		self.filename = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename="com.apple.wifi.plist", domaintype="SystemPreferencesDomain"))

		if (not os.path.isfile(self.filename)):
			raise Exception("Known networks file not found: \"%s\""%self.filename)
		
		#self.ui.listTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		#QtCore.QObject.connect(self.ui.listTree, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.ctxMenu)
		
		if (daemon == False):
		
			self.ui.networksTree.setColumnHidden(0,True)
			QtCore.QObject.connect(self.ui.networksTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onTreeClick)
			
			self.populateUI()


	def populateUI(self):
	
		self.networks = plistutils.readPlist(self.filename)['List of known networks']
		
		index = 0
		for network in self.networks:
		
			element = QtGui.QTreeWidgetItem(None)
			element.setText(0, str(index))			
			element.setText(1, network['SSID'])			
			self.ui.networksTree.addTopLevelItem(element)
			
			index += 1


	def onTreeClick(self):
		
		# retrieving selected network
		currentSelectedElement = self.ui.networksTree.currentItem()
		if (currentSelectedElement): pass
		else: return

		currentSelectedID = int(currentSelectedElement.text(0))
		
		currentNetwork = self.networks[currentSelectedID]
		
		self.ui.labelSSID.clear()
		self.ui.labelBSSID.clear()
		self.ui.labelLastJoined.clear()
		self.ui.labelLastAutoJoined.clear()
		
		if ("SSID" in currentNetwork.keys()):
			self.ui.labelSSID.setText(str(currentNetwork['SSID']))
		if ("BSSID" in currentNetwork.keys()):	
			self.ui.labelBSSID.setText(str(currentNetwork['BSSID']))
		if ("lastJoined" in currentNetwork.keys()):
			self.ui.labelLastJoined.setText(str(currentNetwork['lastJoined']))
		if ("lastAutoJoined" in currentNetwork.keys()):
			self.ui.labelLastAutoJoined.setText(str(currentNetwork['lastAutoJoined']))
		
		self.ui.networkTree.clear()
		self.parseNode(currentNetwork, None)

	def parseNode(self, newNode, parentNode):
	
		if (type(newNode) == type({}) or type(newNode) == plistlib._InternalDict):	
			
			if (parentNode):
				dictNode = QtGui.QTreeWidgetItem(parentNode)
				dictNode.setText(0, "<dict>")
				self.ui.networkTree.addTopLevelItem(dictNode)
				
				for element in newNode:
					titleNode = QtGui.QTreeWidgetItem(dictNode)
					titleNode.setText(0, str(element))
					self.ui.networkTree.addTopLevelItem(titleNode)
					
					self.parseNode(newNode[element], titleNode)
			
			else:
				for element in newNode:
					titleNode = QtGui.QTreeWidgetItem(None)
					titleNode.setText(0, str(element))
					self.ui.networkTree.addTopLevelItem(titleNode)
					
					self.parseNode(newNode[element], titleNode)			
		
		elif (type(newNode) == type([])):
			
			for element in newNode:
				self.parseNode(element, parentNode)
		
		else:
		
			try:
				content = str(newNode)
			except:
				content = newNode.encode("utf8", "replace")		
		
			titleNode = QtGui.QTreeWidgetItem(parentNode)
			titleNode.setText(0, content)
			self.ui.networkTree.addTopLevelItem(titleNode)


def main(cursor, path):
	return KnownNetworksWidget(cursor, path)