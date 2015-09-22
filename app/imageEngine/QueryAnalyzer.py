import os
import cv2
from imageEngine.ColorDescriptor import ColorDescriptor

class QueryAnalyzer:
    def __init__(self, queryPath):
        self.queryPath = queryPath

    def analyze(self):
        print "\nanalysing\n"
        queryImage = cv2.imread(self.queryPath)
        cd = ColorDescriptor((8, 12, 3))
        queryHist = cd.extractHist(queryImage)
        return queryHist
