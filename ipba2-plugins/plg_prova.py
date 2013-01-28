from PySide import QtCore, QtGui
from prova_ui import Ui_Prova

PLUGIN_NAME = "Plugin di Prova by mario"

class ProvaWidget(QtGui.QWidget):
	
	def __init__(self, fileName = None):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_Prova()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.fileName = fileName

	def setTitle(self, title):
		self.setWindowTitle(title)

def main(fileName):
	return ProvaWidget(fileName)