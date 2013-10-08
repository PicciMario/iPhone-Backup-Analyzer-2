# iPBD2 - iPhone Backup Decoder and Analyzer

(C)opyright 2013 Mario Piccinelli <mario.piccinelli@gmail.com>

Released under [MIT licence](http://en.wikipedia.org/wiki/MIT_License)

This software allows the user to browse through the content of an iPhone/iPad backup made by iTunes (or other software able to perform iOS devices' backup). The software is packed with all the routines needed to understand and show the content of files found.

IPBA2 parses the backup directory and shows the decoded filesystem tree. Each file can be clicked to see its properties, such as:

* Real name and name in the backup directory
* File UNIX permissions
* Data hash (as calculated by iOS)
* User and group ID
* Modify time, access time, creation time
* File type (from magic numbers)

Some builtin viewer allow to browse through known file formats (right click on the files in the tree to show a contextual menu):

* ASCII viewer
* PLIST structure browser (both plain and binary ones)
* SQLITE browser
* HEX viewer

The software provides a plugin system to create views showing specific data from the backup. Currently available views:

* Call history

# Development 

Requires:

* Tested on Python 2.7 on Windows 7.

* Python Imaging Library (PIL).
  
* Pyside

* QT

# Running on Linux

* run `make debian` to install the required python libraries.
* run `make build` to build/compile the Qt/UI files (required once)
* run `make run` to start the iPhone Backup Analyzer program.

# Plugins

The plugins system provides an easy way to program additional views to extract and present specific data to the end user. The plugins must adhere to the following standards, and they will be loaded automatically and presented to the user in a menu on the main UI.

The rules are:

* The plugin files are written in python (well, of course :-) )

* The plugin files are placed in the "ipba2-plugins" folder

* The plugin is a single .py file (altought can refer to other files placed in the same directory, if you want).

* The plugin's file name must start with "plg_", such as "plg_test.py"

* The plugin must contain a main method with two parameters, which will be respectively the cursor to the memory database which stores the backup structure and the full path to the backup directory. Something like: "def main(cursor, path):"

* The plugin UI is built in PySide.

* The aforementioned main method MUST return the interface of the plugin as a QtGui.QWidget instance (or a subclass of it).

* The plugin MUST NOT modify the database in any way. Just SELECT statements.

* The plugin MUST adhere to good forensics standards, i.e. no files alteration and so on.

* If you are in doubt, check preexisting plugins.

# Database structure

The core element in iPBA2 is a SQLITE3 database stored in RAM containing the description of the whole backup directory, as acquired during archive parsing during software startup. The database contains a table called "indice", described below.

CREATE TABLE indice ( 
id INTEGER PRIMARY KEY AUTOINCREMENT,
type VARCHAR(1),
permissions VARCHAR(9),
userid VARCHAR(8),
groupid VARCHAR(8),
filelen INT,
mtime INT,
atime INT,
ctime INT,
fileid VARCHAR(50),
domain_type VARCHAR(100),
domain VARCHAR(100),
file_path VARCHAR(100),
file_name VARCHAR(100),
link_target VARCHAR(100),
datahash VARCHAR(100),
flag VARCHAR(100)
