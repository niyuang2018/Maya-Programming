# Scene Information Exporter 2021/10/28
# Traverse over the objects in a .maya scene and export
# performance-related information to .csv or .json file. 

# Can be useful in the QA or profiling process in 
# game development

import sys 
import maya.cmds as mc
import csv
import json

informationContainerList = []

class informationContainer:
	def __init__(self, on, vc, tc, mal):
		self.on = on
		self.vc = vc
		self.tc = tc 
		self.mal = mal

	def toList(self):
		return [self.on, self.vc, self.tc, self.mal]

def getInformation():
	objectsInScene = mc.ls(shapes = True)

	progressWindow = mc.window(title = "Fetching objects...")
	mc.columnLayout()
	progressControl = mc.progressBar(maxValue = len(objectsInScene) - 1, width = 300)
	mc.showWindow(progressWindow)

	for objectInScene in objectsInScene:
		try:
			objectName = objectInScene

			# Vertex Count
			objectVertexCount = mc.polyEvaluate(objectInScene, v = True)

			#Triangle Count
			objectTriangleCount = mc.polyEvaluate(objectInScene, t = True)
					
			# Shading 
			shadingEngine = mc.listConnections(objectInScene, type="shadingEngine")
			materials = mc.ls(mc.listConnections(shadingEngine),materials = True)
		except Exception as e:
			pass

		informationContainerList.append(informationContainer(objectName, objectVertexCount, objectTriangleCount, materials))
		mc.progressBar(progressControl, edit = True,  step= 1)

	mc.deleteUI(progressWindow)

def convertListToDic(list):
	InformationContainerDic = {}

	for inforamtionContainer in informationContainerList:
		InformationContainerDic[inforamtionContainer.on] = {"Object Vertex Count" : inforamtionContainer.vc, "Object Triangle Count" : inforamtionContainer.tc, "Material Attached" : inforamtionContainer.mal}

	return InformationContainerDic

def export2CSV(path):
	with open(path, 'w') as file:
		csv_writer = csv.writer(file, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
		for informationContainer in informationContainerList:
			csv_writer.writerow([unicode(informationContainerToList).encode("utf-8") for informationContainerToList in informationContainer.toList()])

def export2Json(path):
	with open(path, 'w') as file:
		toJsonDump = json.dumps(convertListToDic(informationContainerList), indent = 4)
		file.write(toJsonDump)

class exportWindow():
	def __init__(self):
		if mc.window("exportWindow", query = True, exists = True):
			mc.deleteUI("exportWindow")

		win = mc.window("exportWindow", title = "Export",  widthHeight = (200, 100))
		layout = mc.columnLayout("exportLayout",  adjustableColumn = True, parent = win)
		mc.button("Export to CSV", label = "Export Scene Object to CSV", command = self.onExport2CSV, parent = layout)
		mc.button("Export to Json", label = "Export Scene Object to Json", command = self.onExport2Json, parent = layout)
		mc.showWindow(win)

	def onExport2CSV(self, state):
		csvFilter = "*.csv"
		path = mc.fileDialog2(fileMode=0, fileFilter=csvFilter)
		if not path:
			return
		path = next(iter(path), None)
		getInformation()
		export2CSV(path)

	def onExport2Json(self, state):
		jsonFilter = "*.json"
		path = mc.fileDialog2(fileMode=0, fileFilter=jsonFilter)
		if not path:
			return
		path = next(iter(path), None)
		getInformation()
		export2Json(path)

export2CSVWindow = exportWindow()