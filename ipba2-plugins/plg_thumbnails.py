from PySide import QtCore, QtGui
from thumbsbrowser_ui import Ui_ThumbsBrowser

import os, sqlite3
from datetime import datetime
import struct

PLUGIN_NAME = "Thumbnails Browser"
import plugins_utils

class ThumbsBrowser(QtGui.QWidget):

	frame_width = 160#120
	frame_height = 158#120
	frame_padding = 28

	start = 0
	number = 30

	def __init__(self, cursor, path, daemon = False):
		QtGui.QWidget.__init__(self)
		
		self.ui = Ui_ThumbsBrowser()
		self.ui.setupUi(self)
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
		self.cursor = cursor
		self.backup_path = path
		
		#self.filename = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename="120x120.ithmb"))
#		self.filename = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename="158x158.ithmb"))

		# check if files exist
#		if (not os.path.isfile(self.filename)):
#			raise Exception("Thumbnails file not found: \"%s\""%self.filename)
		
		if (daemon == False):
			self.populateUI()
			QtCore.QObject.connect(self.ui.thumbsFilesList, QtCore.SIGNAL("currentIndexChanged(int)"), self.changeThumbsFile)
			QtCore.QObject.connect(self.ui.buttonLeft, QtCore.SIGNAL("clicked()"), self.pageLeft)			
			QtCore.QObject.connect(self.ui.buttonRight, QtCore.SIGNAL("clicked()"), self.pageRight)			

	def dump(self, src, length=8, limit=10000):
		FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])
		N=0; result=''
		while src:
			s,src = src[:length],src[length:]
			hexa = ' '.join(["%02X"%ord(x) for x in s])
			s = s.translate(FILTER)
			result += "%04X   %-*s   %s\n" % (N, length*3, hexa, s)
			N+=length
			if (len(result) > limit):
				src = "";
				result += "(analysis limit reached after %i bytes)"%limit
		return result
	

	def changeThumbsFile(self):
		
		index = self.ui.thumbsFilesList.currentIndex()
		
		print index
		print len(self.availableThumbFiles)
		
		if (len(self.availableThumbFiles) > index):
		
			element = self.availableThumbFiles[index]
			self.frame_width = element[1]
			self.frame_height = element[2]
			self.frame_padding = element[3]
			self.filename = element[4]
	
			self.drawThumbs(self.start, self.number)

	def pageLeft(self):
		
		if (self.start == 0):
			return
	
		self.start = self.start - self.number
		
		if (self.start < 0):
			self.start = 0
		
		self.drawThumbs(self.start, self.number)

	def pageRight(self):
	
		self.start = self.start + self.number

		self.drawThumbs(self.start, self.number)

	def populateUI(self):
	
		thumbFiles = [
			["120x120.ithmb", 120, 120, 28],
			["158x158.ithmb", 160, 158, 28]
		]
		
		self.availableThumbFiles = []
		
		for file in thumbFiles:
			fileName = file[0]
			width = file[1]
			height = file[2]
			padding = file[3]
			
			searchFile = os.path.join(self.backup_path, plugins_utils.realFileName(self.cursor, filename=fileName))
			if (os.path.isfile(searchFile)):
				file.append(searchFile)
				self.availableThumbFiles.append(file)
		
		index = 0
		for file in self.availableThumbFiles:
			self.ui.thumbsFilesList.insertItem(index, file[0])
			index = index + 1
		
		if (len(self.availableThumbFiles) > 0):
		
			element = self.availableThumbFiles[0]
			self.frame_width = element[1]
			self.frame_height = element[2]
			self.frame_padding = element[3]
			self.filename = element[4]
	
			self.drawThumbs(self.start, self.number)
	
	def drawThumbs(self, start, number):

		self.ui.thumbsTable.clear()
		self.ui.thumbsTable.setRowCount(number)
		self.ui.thumbsTable.setColumnCount(2)
		
		# table header
		newItem = QtGui.QTableWidgetItem("Image")
		self.ui.thumbsTable.setHorizontalHeaderItem(0, newItem)
		newItem = QtGui.QTableWidgetItem("Padding data")
		self.ui.thumbsTable.setHorizontalHeaderItem(1, newItem)
		
		# read file
		f = open(self.filename, 'rb')
		wholefile = f.read()
		f.close()

		# calculate frames size and number
		framelen_image = self.frame_width * self.frame_height *2
		framelen = framelen_image + self.frame_padding
		numframes = len(wholefile) / framelen
		
		# print table rows, one for each frame
		for i in range(start, start + number):
		
			if (len(wholefile) < framelen*(i+1)):
				break
		
			# read frame data from whole file
			string = wholefile[framelen*i : framelen*(i+1) - self.frame_padding]		
			padding = wholefile[framelen*(i+1) - self.frame_padding : framelen*(i+1)-1]
			
			#convert BGR15 to RGB32
			rgb32string = ""
			
			for pixelIndex in range(self.frame_width * self.frame_height):
				
				bgrPixelChars = string[pixelIndex*2:pixelIndex*2+2]				
				bgrPixel = struct.unpack('H', bgrPixelChars)[0]
				
				fill = 0xFF
				b = (bgrPixel >> 10) & 0x1F
				g = (bgrPixel >> 5) & 0x1F
				r = bgrPixel & 0x1F
				
				rgb32string += "%c%c%c%c"%(r<<3, g<<3, b<<3, fill)
			
			# build image with RGB32 string
			qimg = QtGui.QImage(rgb32string, self.frame_width, self.frame_height, QtGui.QImage.Format_RGB32)
			qpix = QtGui.QPixmap.fromImage(qimg).copy()
			qicon = QtGui.QIcon(qpix)
			
			# build the cells in the table row			
			newItem = QtGui.QTableWidgetItem()
			newItem.setIcon(qicon)
			self.ui.thumbsTable.setItem(i-start, 0, newItem)
			
			thumbDescr = "Thumbnail index: %i\nPosition in file: 0x%x"%(i, framelen*i)
			thumbDescr += "\n\nPadding data:\n" + self.dump(padding)

			newItem = QtGui.QTableWidgetItem(thumbDescr)
			self.ui.thumbsTable.setItem(i-start, 1, newItem)
			
			self.ui.thumbsTable.setRowHeight(i-start, self.frame_height + 5)
			
		self.ui.thumbsTable.setIconSize(QtCore.QSize(200,200))
		self.ui.thumbsTable.resizeColumnsToContents()		
		self.ui.thumbsTable.horizontalHeader().setStretchLastSection(True)
		
		self.ui.descriptionLabel.setText("Thumbs %i-%i of 0-%i"%(start, start + number - 1, numframes-1))


def main(cursor, path):
	return ThumbsBrowser(cursor, path)