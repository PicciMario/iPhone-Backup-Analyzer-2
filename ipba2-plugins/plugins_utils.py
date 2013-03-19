#!/usr/bin/env python

'''
 Analyzer for iPhone backup made by Apple iTunes

 (C)opyright 2011 Mario Piccinelli <mario.piccinelli@gmail.com>
 Released under MIT licence
 
'''

# IMPORTS -----------------------------------------------------------------------------------------

import sqlite3, sys, os
from PySide import QtCore, QtGui

# MAIN FUNCTION --------------------------------------------------------------------------------

def realFileName(cursor, filename="", domaintype="", path="", domain=""):
	query = "SELECT fileid FROM indice WHERE 1=1"
	if (filename != ""):
		query = query + " AND file_name = \"%s\""%filename
	if (domaintype != ""):
		query = query + " AND domain_type = \"%s\""%domaintype
	if (domain != ""):
		query = query + " AND domain = \"%s\""%domain
	if (path != ""):
		query = query + "AND file_path = \"%s\""%path

	cursor.execute(query);
	results = cursor.fetchall()
			
	if (len(results) > 0):
		return results[0][0]
	else:
		return ""

def message(text):
	msgBox = QtGui.QMessageBox()
	msgBox.setText(text)
	msgBox.exec_()

def error(text):
	msgBox = QtGui.QMessageBox()
	msgBox.setText(text)
	
	detailedText = "Type: %s"%sys.exc_info()[0].__name__
	detailedText += "\nDescription: %s"%str(sys.exc_info()[1])
	detailedText += "\nFile: %s"%os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]
	detailedText += "\nLine: %s"%str(sys.exc_info()[2].tb_lineno)
	
	msgBox.setDetailedText(detailedText)
	msgBox.exec_()	

def pluginsTempDir():
	tempDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp")
	if (not os.path.isdir(tempDir)):
		os.makedirs(tempDir)
	return tempDir

def pluginTempFile():
	dir = pluginsTempDir()
	base = "pluginTmp"
	index = 0
	fileName = os.path.join(dir, "%s%03i"%(base, index))
	while (os.path.isfile(fileName)):
		fileName = os.path.join(dir, "%s%03i"%(base, index))
		index += 1
	return fileName