import os
import numpy as np
import cv2
import simplejson
from imageEngine.ColorDescriptor import ColorDescriptor
from imageEngine.BoW.TrainModel import TrainModel
from imageEngine.TextAnalyzer import TextAnalyzer


class PreProcessor:
	def __init__(self, DBPath, svmTrainPath):
		self.DBPath = DBPath
		self.svmTrainPath = svmTrainPath
		self.DBExists = os.path.isfile(DBPath)
		self.trainedDataExists = os.path.isfile(svmTrainPath)
		self.cd = ColorDescriptor((8, 12, 3))
		self.MESSAGE_INIT = "loading aria..."
		self.MESSAGE_SUCCESS = "aria ready."

	def isDBMissing(self):
		return (not self.DBExists)

	def isModelUntrained(self):
		return (not self.trainedDataExists)

	def trainData(self, TRAINED_DATA_FOLDER):
		trainModel = TrainModel(TRAINED_DATA_FOLDER)
		print "TRAIN:", TRAINED_DATA_FOLDER
		trainModel.train()

	def processImages(self, imgDBFolder):
		print self.MESSAGE_INIT

		imgInfo = {}

		#root for file access
		#dirs for directory name
		for root, dirs, files in os.walk(imgDBFolder):
			currentDir = root.rsplit('/', 1)[1]

			if len(files) == 50:
				for pic in files:
					if pic not in imgInfo:
						histInfo = self.getHistFeatures(root + '/'+  pic) # color histo info
						histInfo = np.array(histInfo).tolist()
						# print "pic: ", type(pic)
						# print "currentDir: ", type(currentDir)
						# print "hist: ", type(histInfo[0])
						imgInfo[pic] = {"concepts": [currentDir], "histoDetails": histInfo} #tag concepts
					else:
						imgInfo[pic]["concepts"] += [currentDir]

		outputFileName = os.getcwd() + '/static/data/imgInfo.json'

		with open(outputFileName, 'w') as fp:
			simplejson.dump(imgInfo, fp)

		self.trainData(imgDBFolder)
		print self.MESSAGE_SUCCESS
		return True

	def getHistFeatures(self, imgPath):
		image = cv2.imread(imgPath)
		result = self.cd.extractHist(image)
		return result
