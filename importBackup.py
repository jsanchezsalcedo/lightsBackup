'''
LGT BACKUP (Import) v1.0.1
by Jorge Sanchez Salcedo, 2018

Import the backups of the lights of the scene
previously created.
'''

import os
import json
from glob import glob

import maya.cmds as cmds
from maya import OpenMayaUI as omui

try:
	from PySide2 import QtCore, QtWidgets
	from shiboken2 import wrapInstance

except ImportError:
	from PySide import QtCore, QtGui, QtWidgets
	from shiboken import wrapInstance

mainWindow = None
__title__ = 'LGT Backup (Import)'
__version__ = 'v1.0.1'

def getMayaWindow():
	ptr = omui.MQtUtil.mainWindow()
	mainWindow = wrapInstance(long(ptr), QtWidgets.QMainWindow)
	return mainWindow

class ImportBackup(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super(ImportBackup, self).__init__(parent)

		self.setWindowTitle('{} {}'.format(__title__, __version__))
		self.setWindowFlags(QtCore.Qt.Dialog)
		self.setMinimumWidth(320)
		self.setMinimumHeight(300)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

		self.importBackupUI()

	def importBackupUI(self):
		mainLayout = QtWidgets.QVBoxLayout()

		filesLayout = QtWidgets.QVBoxLayout()
		self.filesTable = QtWidgets.QTableWidget()
		self.filesTable.horizontalHeader().setVisible(False)
		self.filesTable.verticalHeader().setVisible(False)
		self.filesTable.setColumnCount(1)
		self.filesTable.setColumnWidth(0, 480)
		self.filesTable.setAlternatingRowColors(True)
		self.filesTable.setSortingEnabled(True)
		self.filesTable.setShowGrid(False)

		filesLayout.addWidget(self.filesTable)

		mainLayout.addLayout(filesLayout)

		self.setLayout(mainLayout)
		self.populate()

	def getBackupFolder(self):
		project = cmds.workspace(q = True, rd = True)
		return project

	def getJsonFiles(self):
		project = self.getBackupFolder()
		jsonFiles = glob(os.path.join(project, 'backup', '*.json'))
		return jsonFiles

	def populate(self):
		print ' '
		print ' > You are running LGT BACKUP (Import) v1.0.1 by JS, 2018.'

		self.filesTable.clearContents()
		jsonFiles = self.getJsonFiles()

		for i in jsonFiles:
			file = i.split('\\')[-1]
			name, ext = os.path.splitext(file)

			item = QtWidgets.QTableWidgetItem(name)
			item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.AlignCenter)

			self.filesTable.insertRow(0)
			self.filesTable.setItem(0, 0, item)

		self.filesTable.itemDoubleClicked.connect(self.importJsonFile)

	def importJsonFile(self):
		project = self.getBackupFolder()
		selectedBackup = self.filesTable.currentItem()
		backupName = selectedBackup.text()
		jsonFile = backupName + '.json'
		backupPath = os.path.join(project, 'backup', jsonFile)
		importFile = json.load(open(backupPath))

		for k,v in importFile.iteritems():
			lgtName = k
			lgtTrans = v
			for k, v in lgtTrans.iteritems():
				attr = lgtName + ('.') + k
				try:
					cmds.setAttr(attr, v)
				except RuntimeError:
					continue

		print '   > You just import LGT backup from:'
		print '    ', backupPath
		print ' '

def run():
	global mainWindow
	if not mainWindow or not cmds.window(mainWindow, q=True, e=True):
		mainWindow = ImportBackup(parent=getMayaWindow())
	mainWindow.show()