# Texture Color Balance Serializer 2021/10/25
# Read, save and load color balance values of a selected texture
# Can be useful when manipulating the imported values of textures in maya

import maya.cmds as mc
import json

values = {
	'exposure',
	'defaultColor',
	'colorGain',
	'colorOffset',
	'alphaGain',
	'alphaOffset',
	'alphaIsLuminance'
}

dic = {}

def setColorBalanceAttributes(texture, data):
	for value in values:
		if (type(data.get(value)) is list):
			mc.setAttr('%s.%s'%(texture[0], value), data.get(value)[0][0],data.get(value)[0][1],data.get(value)[0][2])
		else:
			mc.setAttr('%s.%s'%(texture[0], value), data.get(value))
	
def getColorBalanceAttributes():
	texture = getCurrentSelectedTexture()

	for value in values:
		dic[value] = mc.getAttr('%s.%s'%(texture[0], value))
	return dic

def getCurrentSelectedTexture():
	return checkIfCurrentSelectedIsATexture(mc.ls(selection = True))

def checkIfCurrentSelectedIsATexture(selection):
	if (mc.getClassification(mc.objectType(selection),satisfies="texture")) is True or len(selection) != 1:
		mc.confirmDialog( message = 'What you select is not a texture or you have selected multiple texture')
	else:
		return selection
		
def clear():
	dic = {}

def saveAsJson(dictionary, path):
	with open(path, 'w') as file:
		toJsonDump = json.dumps(dictionary, indent = 4)
		file.write(toJsonDump)

def loadJson(path):
	with open(path, 'r') as file:
		data = json.load(file)
	return data

class setColorBalanceWindow():
	def __init__(self):
		if mc.window("colorBalanceWindow", query = True, exists = True):
			mc.deleteUI("colorBalanceWindow")

		win = mc.window("colorBalanceWindow", title = "Color Balance",  widthHeight = (200, 100))
		layout = mc.columnLayout("colorBalanceWindow",  adjustableColumn = True, parent = win)
		mc.button("Save as Json", label = "Save Color Balance as Json", command = self.save, parent = layout)
		mc.button("Load a Json", label = "Load a Json file as Color Balance", command = self.load, parent = layout)
		mc.showWindow(win)

	def save(self, state):
		jsonFilter = "*.json"
		path = mc.fileDialog2(fileMode=0, fileFilter=jsonFilter)
		if not path:
			return
		path = next(iter(path), None)
		file = getColorBalanceAttributes()

		saveAsJson(file, path)
		clear()

	def load(self, state):
		clear()
		jsonFilter = "*.json"
		path = mc.fileDialog2(fileMode=1, fileFilter=jsonFilter)
		if not path:
			return
		path = next(iter(path), None)

		texture = getCurrentSelectedTexture();
		data = loadJson(path)

		setColorBalanceAttributes(texture, data)

colorBalanceSerializer = setColorBalanceWindow()

