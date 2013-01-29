#!/usr/bin/env python

'''
 Analyzer for iPhone backup made by Apple iTunes

 (C)opyright 2011 Mario Piccinelli <mario.piccinelli@gmail.com>
 Released under MIT licence
 
'''

# IMPORTS -----------------------------------------------------------------------------------------

import sqlite3

# MAIN FUNCTION --------------------------------------------------------------------------------

def realFileName(cursor, filename="", domaintype="", path=""):
	query = "SELECT fileid FROM indice WHERE 1=1"
	if (filename != ""):
		query = query + " AND file_name = \"%s\""%filename
	if (domaintype != ""):
		query = query + " AND domain_type = \"%s\""%domaintype
	if (path != ""):
		query = query + "AND file_path = \"%s\""%path

	cursor.execute(query);
	results = cursor.fetchall()
			
	if (len(results) > 0):
		return results[0][0]
	else:
		print("ERROR: could not find file")
		return ""