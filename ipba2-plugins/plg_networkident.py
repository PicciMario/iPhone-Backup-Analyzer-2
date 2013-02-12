from PySide import QtCore, QtGui
from networkident_ui import Ui_NetworkIdent

import os, sqlite3
from datetime import datetime

PLUGIN_NAME = "Network Identification"
import plugins_utils

# retrieve modules from ipba root directory
import plistutils

class NetworkIdentWidget(QtGui.QWidget):
	
	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_NetworkIdent()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		self.filename = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename="com.apple.network.identification.plist", domaintype="SystemPreferencesDomain"))

		if (not os.path.isfile(self.filename)):
			raise Exception("Network Identification file not found: \"%s\""%self.filename)
		
		QtCore.QObject.connect(self.ui.networksTree, QtCore.SIGNAL("itemSelectionChanged()"), self.onTreeClick)
		self.ui.networksTree.setColumnHidden(0,True)
		
		if (daemon == False):
			self.populateUI()

	def populateUI(self):
		
		signatures = plistutils.readPlist(self.filename)['Signatures']
		
		index = 0
		for element in signatures:
			ident = element['Identifier']
			identParts = ident.split(";")
			if (len(identParts) == 1):
				ident = identParts[0]
			else:
				ident = identParts[1].split("=")[1]
			
			timestamp = element['Timestamp']
			timestamp = timestamp.strftime('%b %d %Y %H:%M UTC')

			newElement = QtGui.QTreeWidgetItem(None)
			newElement.setText(0, str(index))
			newElement.setText(1, ident)
			newElement.setText(2, str(timestamp))
			self.ui.networksTree.addTopLevelItem(newElement)
			
			index += 1

	def onTreeClick(self):
		
		# retrieving selected network
		currentSelectedElement = self.ui.networksTree.currentItem()
		if (currentSelectedElement): pass
		else: return
		
		signatures = plistutils.readPlist(self.filename)['Signatures']
		
		currentNetworkIndex = int(currentSelectedElement.text(0))
		currentNetworkServices = signatures[currentNetworkIndex]['Services']
		
		networkDescr = signatures[currentNetworkIndex]['Identifier']
		networkDescrParts = networkDescr.split(";")
		networkDescr = "\n".join(networkDescrParts)
		self.ui.networkLabel.setText(networkDescr)
		
		self.ui.servicesTree.clear()
		
		for service in currentNetworkServices:
			
			serviceNode = QtGui.QTreeWidgetItem(None)
			serviceNode.setText(0, "service")
			self.ui.servicesTree.addTopLevelItem(serviceNode)
			serviceNode.setExpanded(True)
			
			for serviceKey in service.keys():
				
				subserviceNode = QtGui.QTreeWidgetItem(serviceNode)
				subserviceNode.setText(0, serviceKey)
				self.ui.servicesTree.addTopLevelItem(subserviceNode)
				subserviceNode.setExpanded(True)

				if (serviceKey == "ServiceID"): 
					subserviceNode.setText(1, service['ServiceID'])
					continue
				
				for element in service[serviceKey].keys():
				
					elementNode = QtGui.QTreeWidgetItem(subserviceNode)
					elementNode.setText(0, element)
					text = service[serviceKey][element]
					if (type(text) == type([1,2])):
						text = ", ".join(text)
					elementNode.setText(1, text)
					self.ui.servicesTree.addTopLevelItem(elementNode)
					elementNode.setExpanded(True)

def main(cursor, path):
	return NetworkIdentWidget(cursor, path)