DEBIAN_PACKAGES=python-dev \
		python-qt4 python-qt4-dev python-qt4-doc \
		python-pyside pyside-tools

# These are the input UI (XML) files
UI_FILES=about_window.ui \
	hex_widget.ui \
	image_widget.ui \
	main_window.ui \
	plist_widget.ui \
	sqlite_widget.ui \
	text_widget.ui \
	ipba2-plugins/addressbook_ui.ui \
	ipba2-plugins/callhistory_ui.ui \
	ipba2-plugins/general_ui.ui \
	ipba2-plugins/knownnetworks_ui.ui \
	ipba2-plugins/networkident_ui.ui \
	ipba2-plugins/note_ui.ui \
	ipba2-plugins/safarihistory_ui.ui \
	ipba2-plugins/safaristate_ui.ui \
	ipba2-plugins/safbookmarks_ui.ui \
	ipba2-plugins/skype_ui.ui \
	ipba2-plugins/sms_ui.ui \
	ipba2-plugins/thumbsbrowser_ui.ui \
	ipba2-plugins/viber_ui.ui \
	ipba2-plugins/whatsapp_ui.ui


# These are the compiled(generated) output files.
PY_UI_FILES=$(UI_FILES:.ui=.py)

# This is the input file
QRC_FILE=resources.qrc
# These is the output file (NOTE: the file name is different)
RC_FILE=resources_rc.py

# Would these work on windows?
PYSIDE_UIC=pyside-uic
PYSIDE_RCC=pyside-rcc

all: help

# Default target
# Show basic help to the user
.PHONY: help
help:
	@echo ""
	@echo "--== iPhone-Backup-Analyzer-2 ==--"
	@echo "website: http://www.ipbackupanalyzer.com/"
	@echo "source code: https://github.com/PicciMario/iPhone-Backup-Analyzer-2"
	@echo ""
	@echo "Options:"
	@echo "   $$ make debian  -  Installed required Python packages,"
	@echo "                     on Debian and Ubuntu."
	@echo "   $$ make build   -  Build/Compile files"
	@echo "   $$ make run     -  Runs the iPhone Backup Explorer"
	@echo "   $$ make clean   -  Remove compiled files"
	@echo ""

.PHONY: build
build: ui rc

##
## Compile UI files into Python
##
.PHONY: ui
ui: $(PY_UI_FILES)

$(PY_UI_FILES): %.py: %.ui
	$(PYSIDE_UIC) -o "$@" "$<"


##
## Build Resource files.
##
.PHONY: rc
rc: $(RC_FILE)

$(RC_FILE): $(QRC_FILE)
	$(PYSIDE_RCC) -o "$@" "$<"


##
## Clean up
##
.PHONY: clean
clean:
	rm -f $(PY_UI_FILES) $(RC_FILE)

##
## Helper target to run the program
## (saves the little trouble of typing "python" or using "chmod")
.PHONY: run
run: build
	python main.py

##
## Helper target to install required packages on debian
##
.PHONY: debian
debian:
	@sudo -p "Enter SUDO passwod to install pyQT4/PySide packages: " \
		apt-get install $(DEBIAN_PACKAGES)
