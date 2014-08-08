#!/usr/bin/python
#
# proxyswitcher.py
# 
# Save proxy settings
# Set/unset proxy settings when selected
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

# GUI setup
class ProxySwitcher(QWidget):
    def __init__(self):
        super(ProxySwitcher, self).__init__()

        self.initUI()

    def initUI(self):

        # Exit Button
        self.exit_btn = QPushButton('Exit', self)
        self.exit_btn.setMaximumSize(50,30)

        self.controlsLayout = QGridLayout()
        self.controlsLayout.addWidget(self.exit_btn, 3, 3)
        self.setLayout(self.controlsLayout)

       

class ProxySwitcherWindow(QMainWindow):
    def __init__(self):
        super(ProxySwitcherWindow, self).__init__()
        self.widget = ProxySwitcher()
        self.setCentralWidget(self.widget)

        #Create Menu Item
        self.createAction = QAction(QIcon('create.png'), '&Create', self)
        self.createAction.setShortcut('Ctrl+C')
        self.createAction.setStatusTip('Create Proxy Settings')
        #self.createAction.triggered.connect(self.create)

        #Edit Menu Item
        self.editAction = QAction(QIcon('edit.png'), '&Edit', self)
        self.editAction.setShortcut('Ctrl+E')
        self.editAction.setStatusTip('Edit Proxy Settings')
        self.editAction.triggered.connect(self.openFile)

        #Delete Menu Item
        self.deleteAction = QAction(QIcon('delete.png'), '&Delete', self)
        self.deleteAction.setShortcut('Ctrl+D')
        self.deleteAction.setStatusTip('Delete Proxy Settings')
        #self.deleteAction.triggered.connect(self.delete)

        self.menu = self.menuBar()
        self.proxyMenu = self.menu.addMenu('&Proxy')
        self.proxyMenu.addAction(self.createAction)
        self.proxyMenu.addAction(self.editAction)
        self.proxyMenu.addAction(self.deleteAction)
        self.setGeometry(300, 300, 250, 250)
        self.setWindowTitle('Proxy Switcher')
        self.setWindowIcon(QIcon('switch.png'))

    # open file
    def openFile(self):
        dialog = QFileDialog(self)
        dialog.setDirectory('/home/')
        dialog.setNameFilter('*.pxs')
        dialog.setViewMode(QFileDialog.List)
        if dialog.exec_():
            filename = dialog.selectedFiles()
        #filename = QFileDialog.getOpenFileName(self,'Open Proxy Settings File',
         #                                  '/home/')
 

def main():

    # create a Qt application
    app = QApplication(sys.argv)
    #gui = ProxySwitcher()
    window = ProxySwitcherWindow()
    window.show()

    # Enter Qt application loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# check see if any proxy settings stored



# save file

# open settings file

# close (and save) settings file

# load current proxy settings


# get proxy settings from GUI

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

# set proxy settings
# call get
# parse variables
# export environment variables
# create aptconf file using parsed variables
# save/overwrite aptconf file

# unset proxy settings
# unset environment variables
# create blank aptconf file
# save/overwrite aptconf file
