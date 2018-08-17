'''
LGT BACKUP (Create) v1.0.1
by Jorge Sanchez Salcedo, 2018

Create a backup of the lights of the scene.
'''

import maya.cmds as cmds

import os
import time
import json

class CreateBackup:
	def __init__(self):

		self.createBackup()

	def getLights(self):
		lgtShapes = cmds.ls(dag = True, lt = True)
		lgtTrans = cmds.listRelatives(lgtShapes, p = True)

		return lgtShapes, lgtTrans

	def getTransformAttr(self):
		lgtShapes, lgtTrans = self.getLights()
		transformAttr = {}

		for light in sorted(lgtTrans):
			transformAttr[light] = {
				'translateX':'','translateY':'','translateZ':'',
				'rotateX':'','rotateY':'','rotateZ':'',
				'scaleX':'','scaleY':'','scaleZ':'',
				'visibility':''
			}

			for k, v in transformAttr[light].iteritems():
				attr = light + ('.') + k
				val = cmds.getAttr(attr)
				transformAttr[light][k] = val

		return transformAttr

	def getShapeAttr(self):
		lgtShapes, lgtTrans = self.getLights()
		shapeAttr = {}

		for light in sorted(lgtShapes):
			shapeAttr[light] = {
				'colorR':'', 'colorG':'', 'colorB':'',
				'intensity':'', 'coneAngle':'', 'penumbraAngle':'',
				'dropoff':'', 'aiExposure':'', 'aiSpread':'',
				'aiRoundness':'', 'aiSoftEdge':'', 'aiAngle':'',
				'aiRadius':''
				}

			for k, v in shapeAttr[light].iteritems():
				attr = light + ('.') + k
				try:
					val = cmds.getAttr(attr)
				except ValueError:
					continue
				shapeAttr[light][k] = val

		return shapeAttr

	def getSceneName(self):
		project = cmds.workspace(q = True, rd = True)

		sceneFolder = cmds.workspace(q = True, dir = True)
		sceneName = cmds.file(q = True, sn = True, shn = True)
		name, ext = os.path.splitext(sceneName)
		scenePath = os.path.join(sceneFolder, sceneName)

		getDate = time.gmtime(os.path.getmtime(scenePath))
		sceneDate = str(time.strftime('%Y%m%d', getDate))
		sceneHour = str(time.strftime('%H%M', getDate))

		return project, sceneDate, name, sceneHour

	def createDB(self):
		transformAttr = self.getTransformAttr()
		shapeAttr = self.getShapeAttr()
		db = {}
		db.update(transformAttr)
		db.update(shapeAttr)

		return db

	def createBackupFolder(self):
		project, sceneDate, name, sceneHour = self.getSceneName()
		os.mkdir(os.path.join(project, 'backup'))
		self.createBackup()

	def createBackup(self):

		print ' '
		print ' > You are running LGT BACKUP (Create) v1.0.1 by JS, 2018.'

		project, sceneDate, name, sceneHour = self.getSceneName()
		db = self.createDB()
		ext = '.json'

		backupName = sceneDate + '-' + name + '-' + sceneHour + ext
		backupPath = os.path.join(project, 'backup', backupName)

		try:
			json.dump(db, fp=open(backupPath, 'w'), indent=4)
		except IOError:
			self.createBackupFolder()

		print '   > You just create the backup of LGT at:'
		print '    ', backupPath
		print ' '