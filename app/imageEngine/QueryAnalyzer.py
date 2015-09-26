import os
import cv2
from imageEngine.ColorDescriptor import ColorDescriptor
from imageEngine.BoW.TrainModel import TrainModel

class QueryAnalyzer:
    def __init__(self, queryPath):
    	print "\nanalysing\n"
        self.queryPath = queryPath

    def analyze(self, flag):
    	# print "\nanalysing\n"
		if flag == "color":
			queryImage = cv2.imread(self.queryPath)
			cd = ColorDescriptor((8, 12, 3))
			queryHist = cd.extractHist(queryImage)
		elif flag == "visual":
			uploadLocation =  "static/upload/"
			# print uploadLocation
			t = TrainModel(uploadLocation, "analyze")
			queryHist = t.uploadAnalysis()
		
		# print "query", queryHist
		return queryHist
