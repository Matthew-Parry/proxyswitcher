#!/usr/bin/python
#
# proxyswitcher.py
# 
# Save proxy settings
# Set/unset proxy settings when selected
#
# ProxySwitcher creates a directory home/ProxySwitcher/
# ProxySwitcher creates a settings file home/ProxySwitcher/settings.pxs
# This file contains:
#		 - current proxy settings
#		 - saved proxy settings
#
# Matthew Parry 2014
#
# -----------------------
# Import required Python libraries
# -----------------------
import time
import os
import sys
from PySide.QtCore import *
from PySide.QtGui import*
import configparser

# GUI setup
class ProxySwitcher(QWidget):
	def __init__(self):
		super(ProxySwitcher, self).__init__()

		self.initUI()

	def initUI(self):

		# Exit Button
		self.delete_btn = QPushButton('Delete', self)
		self.delete_btn.setMaximumSize(50,30)
		self.delete_btn.setEnabled(True)
		self.delete_btn.clicked.connect(self.delete_buttonClicked)
		# Save Button
		self.save_btn = QPushButton('Save', self)
		self.save_btn.setMaximumSize(50,30)
		self.save_btn.setEnabled(False)
		self.save_btn.clicked.connect(self.save_buttonClicked)
		# Set Button
		self.set_btn = QPushButton('Set', self)
		self.set_btn.setMaximumSize(50,30)
		self.set_btn.setEnabled(True)
		self.set_btn.clicked.connect(self.set_buttonClicked)
		# New Button
		self.new_btn = QPushButton('New', self)
		self.new_btn.setMaximumSize(50,30)
		self.new_btn.setEnabled(True)
		self.new_btn.clicked.connect(self.new_buttonClicked)
		# Edit Button
		self.edit_btn = QPushButton('Edit', self)
		self.edit_btn.setMaximumSize(50,30)
		self.edit_btn.setEnabled(True)		
		self.edit_btn.clicked.connect(self.edit_buttonClicked)
		
		#Section
		self.section_lbl = QLabel("Choose:", self)
		self.section_combo = QComboBox(self)
		
		#now load combo box
		savedproxies = proxies.getAllProxies()
		for ProxySetting in savedproxies:
			self.section_combo.addItem(ProxySetting.label)
			
		#call function on selection in combo
		self.section_combo.activated[str].connect(self.comboActivated)  

		self.info_lbl = QLabel("Select Proxy Setting and click Set to use those settings", self)
		self.info2_lbl = QLabel("or Edit to change or Delete to remove or New to create new settings", self)

		#Server
		self.server_lbl = QLabel("Server", self)
		self.server_input = QLineEdit("http://", self)
		self.server_input.setReadOnly(True)

		#Port
		self.port_lbl = QLabel("Port", self)
		self.port_input = QLineEdit("", self)
		self.port_input.setReadOnly(True)

		#Username
		self.username_lbl = QLabel("Username", self)
		self.username_input = QLineEdit("", self)
		self.username_input.setReadOnly(True)

		#Password
		self.password_lbl = QLabel("Password", self)
		self.password_input = QLineEdit("", self)
		self.password_input.setReadOnly(True)

		self.controlsLayout = QGridLayout()
		self.controlsLayout.setSpacing(10)
		self.controlsLayout.addWidget(self.delete_btn, 6, 3)
		self.controlsLayout.addWidget(self.edit_btn, 4, 3)
		self.controlsLayout.addWidget(self.set_btn, 2, 3)
		self.controlsLayout.addWidget(self.new_btn, 3, 3)
		self.controlsLayout.addWidget(self.save_btn, 5, 3)
		self.setLayout(self.controlsLayout)
		
		#labels
		self.controlsLayout.addWidget(self.info_lbl, 0, 0, 1, 2)
		self.controlsLayout.addWidget(self.info2_lbl, 1, 0, 1, 2)
		self.controlsLayout.addWidget(self.section_lbl, 2, 0)
		self.controlsLayout.addWidget(self.section_combo, 2, 1)
		self.controlsLayout.addWidget(self.server_lbl, 3, 0)
		self.controlsLayout.addWidget(self.server_input, 3, 1)
		self.controlsLayout.addWidget(self.port_lbl, 4, 0)
		self.controlsLayout.addWidget(self.port_input, 4, 1)
		self.controlsLayout.addWidget(self.username_lbl, 5, 0)
		self.controlsLayout.addWidget(self.username_input, 5, 1)
		self.controlsLayout.addWidget(self.password_lbl, 6, 0)
		self.controlsLayout.addWidget(self.password_input, 6, 1)
		
		self.comboActivated()
		
	def comboActivated(self):
		#triggered on combo selction
		#get index of selected combo
		savedproxies = proxies.getAllProxies()
		for ProxySetting in savedproxies:		
			if ProxySetting.label == self.section_combo.itemText(self.section_combo.currentIndex()):
				self.server_input.setText(ProxySetting.server)
				self.port_input.setText(ProxySetting.port)
				self.username_input.setText(ProxySetting.username)
				self.password_input.setText(ProxySetting.password)
				if ProxySetting.label == "No Proxy":
					#disable delete and edit buttons
					self.edit_btn.setEnabled(False)
					self.delete_btn.setEnabled(False)
				else:
					#enable delete and edit buttons
					self.edit_btn.setEnabled(True)
					self.delete_btn.setEnabled(True)

	
				
	def edit_buttonClicked(self):
		#allow fields to be edited
		self.server_input.setReadOnly(False)
		self.server_input.setFocus()
		self.port_input.setReadOnly(False)
		self.username_input.setReadOnly(False)
		self.password_input.setReadOnly(False)
		#disable edit and set button
		self.edit_btn.setEnabled(False)
		self.set_btn.setEnabled(False)
		self.new_btn.setEnabled(False)
		#enable save button
		self.save_btn.setEnabled(True)
		
	def delete_buttonClicked(self):
		#exit app
		print("delete")
		#dialog to check delete label for proxy
		msgBox = QMessageBox()
		proxyText = "Delete Proxy Settings for: " + self.section_combo.itemText(self.section_combo.currentIndex())
		msgBox.setWindowTitle("Delete?")
		msgBox.setText(proxyText)
		msgBox.setInformativeText("Do you want to delete these settings?")
		msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		msgBox.setDefaultButton(QMessageBox.No)
		ret = msgBox.exec_()
		
		if ret == QMessageBox.Yes:
			print("DEl")

		
	def set_buttonClicked(self):
		#set app
		print("set")
		# get proxy settings from GUI
		#validate - call validateProxy only if not "No Proxy"
		if self.section_combo.itemText(self.section_combo.currentIndex()) != "No Proxy":
			self.validateProxy()
		#if "No Proxy" then call unsetProxy
		if self.section_combo.itemText(self.section_combo.currentIndex()) == "No Proxy":
			self.unsetProxy()
		else:
			#else call setProxy
			self.setProxy()
		
		
	def unsetProxy(self):
		print("unsetting")
		msgBox = QMessageBox()
		msgBox.setWindowTitle("No Proxy")
		msgBox.setText("Setting to 'No Proxy' will remove ALL proxy settings")
		msgBox.setInformativeText("Do you wish to remove ALL proxy settings?")
		msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		msgBox.setDefaultButton(QMessageBox.No)
		ret = msgBox.exec_()
		if ret == QMessageBox.Yes:
			print("unsetting")
			# unset environment variables
			#to get around child process (us) not being able to amend parent 
			#we need to create a shell file with export commands
			#and then chmod it and run it from here
			envText = "sudo unset http_proxy https_proxy ftp_proxy HTTP_PROXY HTTPS_PROXY FTP_PROXY"
			self.exportEnvVarianbles(envText)
			# create blank aptconf file
			aptconfFile = open(aptconfFilename, 'w')	#overwrites if exists
			# save/overwrite aptconf file
			aptconfFile.close()	#just close it
			#That's it - so let user know ...
			msgBox.setText("Setting to 'No Proxy' processed")
			msgBox.setInformativeText("ALL proxy settings have been removed")
			msgBox.setStandardButtons(QMessageBox.Ok)
			ret = msgBox.exec_()
		else:
			#just return
			msgBox.setText("Setting to 'No Proxy' cancelled")
			msgBox.setInformativeText("")
			msgBox.setStandardButtons(QMessageBox.Ok)
			ret = msgBox.exec_()


		
	def setProxy(self):
		print("setting")
		# set proxy settings
		# parse variables
		aptText = "http://"
		if self.username_input.text():
			#there is a username (and assume password too)
			aptText = aptText + self.username_input.text() + ":" + self.password_input.text() + "@"
		aptText = aptText + self.server_input.text() + ":" + self.port_input.text() + "/"
		print(aptText)
		# export environment variables
		#to get around child process (us) not being able to amend parent 
		#we need to create a shell file with export commands
		#and then chmod it and run it from here
		
		envText = "set http_proxy=" + aptText
		self.exportEnvVarianbles(envText)
		# create aptconf file using parsed variables
		# save/overwrite aptconf file

	def exportEnvVarianbles(self, envText):
		#to get around child process (us) not being able to amend parent 
		#we need to create a shell file with export commands
		#and then chmod it and run it from here
		#open file
		print("exporting")
		envShellFile = open(envShellFilename, 'w')
		envShellFile.write(envText)
		st = os.stat(envShellFilename)
		os.chmod(envShellFilename,0o777)
		envShellFile.close()
		#now run it
#		os.system("sudo ./" + envShellFilename)
		os.system(envShellFilename)
		
	
	def new_buttonClicked(self):
		#new app
		print("new")
		#dialog to enter new label for proxy
		text, ok = QInputDialog.getText(self, 'New Proxy Settings', 
			'Enter label:')
	
		if ok:
			#add to combo box
			self.section_combo.addItem(str(text))
			#set to new entry
			self.section_combo.setCurrentIndex(self.section_combo.count()-1)
			#delete values in edit fields
			self.server_input.setText("")
			self.port_input.setText("80")
			self.username_input.clear()
			self.password_input.clear()
			#then call edit function
			self.edit_buttonClicked()

	def save_buttonClicked(self):
		#save app
		print("save")
		#validate - call validateProxy only if not "No Proxy"
		if self.section_combo.itemText(self.section_combo.currentIndex()) != "No Proxy":
			self.validateProxy()
		#save details into proxy class
		
		
		#switch button states back
		self.edit_btn.setEnabled(True)
		self.set_btn.setEnabled(True)
		self.new_btn.setEnabled(True)
		self.save_btn.setEnabled(False)
		#swicth back input states
		self.server_input.setReadOnly(True)
		self.port_input.setReadOnly(True)
		self.username_input.setReadOnly(True)
		self.password_input.setReadOnly(True)

	def validateProxy(self):
		print("validating")
		
		#server must exist and be text
		serverText = self.server_input.text()
		while not serverText:	#that is while not empty
			msgText = "Server must not be empty - please enter details:"
			serverText, ok = QInputDialog.getText(self, 'Error', msgText)
		#save portTest back to lineedit
		self.server_input.setText(serverText)
		#server must NOT begin with http://or https://
		while serverText.startswith("http://") or serverText.startswith("https://"):
			msgText = "Server must NOT begin with 'http://' or 'https://':"
			serverText, ok = QInputDialog.getText(self, 'Error', msgText ,text=serverText)
		#save portTest back to lineedit
		self.server_input.setText(serverText)
			

		#port must exist and be numeric
		portText = self.port_input.text()
		while not portText.isdigit(): # this is a builtin method of all str objects			print("Error")
			#dialog to edit port
			if not portText:
				portText = "  "
			msgText = "Port (" + portText + ") is not numeric - please enter a number:"
			portText, ok = QInputDialog.getText(self, 'Error', msgText)
		#save portTest back to lineedit
		self.port_input.setText(portText)

		#username does not have to exist
		#password does not have to exist



class ProxySwitcherWindow(QMainWindow):
	def __init__(self):
		super(ProxySwitcherWindow, self).__init__()
		self.widget = ProxySwitcher()
		self.setCentralWidget(self.widget)

		self.setWindowTitle('Proxy Switcher')
		self.setWindowIcon(QIcon('switch.png'))

			
class ProxySetting():
	def __init__(self, label, server, port, username, password):
		self.label = label
		self.server = server
		self.port = port
		self.username = username
		self.password = password
		
	def amend_settings(self, label, server, port, username, password):
		print("amending settings")
		self.label = label
		self.server = server
		self.port = port
		self.username = username
		self.password = password
	
	def printproxy(self):
		print("label = ", self.label)
		print("server = ", self.server)
		print("port = ", self.port)
		print("username = ", self.username)
		print("password = ", self.password)
		
class ProxySettingsArray():
	def __init__(self, settings):
		self.settings = []
		for label, server, port, username, password in settings:
			self.add_settings(label, server, port, username, password)
	
	def add_settings(self,label, server, port, username, password):
		index = self.exists(label)  #returns index of existing entry
		if index > -1:
			#already exists so amend existing values
			self.settings[index].amend_settings(label, server, port, username, password)
			return "label exists"
		else:
			self.settings.append(ProxySetting(label, server, port, username, password))
			return "label appended"
			
	def delete_settings(self,label):
		index = self.exists(label)
		if index > -1:
			#exists so delete
			print("Are you sure?")
			del self.settings[index]
		else:
			return "It don't exist"
			
	def exists(self, label):
		for setting in self.settings:
			if label == setting.label:
				return self.settings.index
		return -1
			
	def printAllProxies(self):
		for setting in self.settings:
			setting.printproxy()
			
	def getAllProxies(self):
		return self.settings


#declaration of variables

settingdirectory =  'c://home/ProxySwitcher/'
settingfilename = settingdirectory + 'settings.pxs'
proxyservername = ""
proxyserverport = ""
proxyuser = ""
proxypassword = ""
proxies = ProxySettingsArray("")	#global
aptconfDirectory = "c://home/ProxySwitcher/"
aptconfFilename = aptconfDirectory + "apt.conf"
envShellFilename = settingdirectory + "setEnv.bat"

def main():

	# check see if any proxy settings stored
	# first check path exists ...
	if not os.path.exists(settingdirectory): #checks for whether this path (pointed by dir), exists or not
		os.makedirs(settingdirectory)           #make it
		
	# now see if we have a settings.pxs file - if not auto create it
	settingsfile = open(settingfilename, 'a')

	#point to global empty array to hold settings
	global proxies
	
	# read file and store sections in array
	if os.path.getsize(settingfilename) > 0:
		#file has data in it
		proxyconfig = configparser.ConfigParser()
		proxyconfig.read(settingfilename)
		for section_name in proxyconfig.sections():
			sectionname = section_name
			servername = proxyconfig.get(section_name,'server')
			portid = proxyconfig.get(section_name,'port')
			username = proxyconfig.get(section_name,'username')
			passwd = proxyconfig.get(section_name,'password')
			#add to array
			proxies.add_settings(sectionname, servername, portid, username, passwd)
	else:
		#else file is zero bytes - hence empty
		#will be first time run - so create blank entry for no proxy
		proxies.add_settings("No Proxy", "","","","")
#		proxies.add_settings("work", "webshield.embc.uk.com","80","","")
	
	# create a Qt application for gui
	app = QApplication(sys.argv)
	window = ProxySwitcherWindow()

	window.show()

	# Enter Qt application loop - process the gui
	app.exec_()
	
	#window has closed
	#save config file - open file for writing
	settingsfile = open(settingfilename, 'w')
	
	#remove all sections
	proxyconfig = configparser.ConfigParser()
	proxyconfig.read(settingfilename)
	for section_name in proxyconfig.sections():
		proxyconfig.remove_section(section_name)

	#now add class info
	savedproxies = proxies.getAllProxies()	#get list of all proxies

	#now save to config file
	for ProxySetting in savedproxies:
		proxyconfig.add_section(ProxySetting.label)
		proxyconfig.set(ProxySetting.label, "server", ProxySetting.server)
		proxyconfig.set(ProxySetting.label, "port", ProxySetting.port)
		proxyconfig.set(ProxySetting.label, "username", ProxySetting.username)
		proxyconfig.set(ProxySetting.label, "password", ProxySetting.password)
	proxyconfig.write(settingsfile)

	#end program
	sys.exit()
	


if __name__ == '__main__':
	main()








# save proxy settings in file
# parse string
# save as file

# edit proxy settings
# call get
# call save

# get proxy settings from file
# find file
# read file into variables

# delete proxy settings
# call get
# delete it if sure




