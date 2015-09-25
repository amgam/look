# import the necessary packages
import numpy as np
import simplejson
import cv2
import numpy as np
from scipy.spatial import distance as dist


class ImageComparator:

	def __init__(self, indexPath):
		# store our index path
		self.indexPath = indexPath
		self.queryHist = ""

	def euclideanDistance(self, queryHist, otherHist):
		otherHist = np.asarray(otherHist)
		return np.linalg.norm(queryHist - otherHist)

	def visualDistance(self, queryHist, otherHist):
		otherHist = np.asarray(otherHist)
		return dist.cosine(queryHist, otherHist)

	def compareAgainstDB(self, queryFeatures, flag, limit = 20):
		# initialize our dictionary of results
		results = {}

		with open(self.indexPath) as imgInfo:
			queryDict = simplejson.load(imgInfo)

		# queryDict = simplejson.loads(open(self.indexPath, "rb"))
		for imgName, info in queryDict.iteritems():

			if flag == "color":
				#Color Hist Comparsion
				features = info["histoDetails"]
				distance = self.visualDistance(queryFeatures, features) 
				results[imgName] = distance
			elif flag == "visual":
				#Visual Hist
				visualHist = info["visualHist"]
				# print "EDMUND:", len(visualHist)
				distance = self.visualDistance(queryFeatures, visualHist)
				results[imgName] = distance

		print "DING", len(results)
		return results
		# results = sorted([(v, k) for (k, v) in results.items()])
		# return results[:limit]
		# return results

	def distIntersection(self, queryHist, otherHist):
		queryHist = np.asarray(queryHist)
		otherHist = np.asarray(otherHist)

		return cv2.compareHist(queryHist, otherHist, cv2.cv.CV_COMP_INTERSECT)

	@np.vectorize
	def weightResults(color, visualKey):
		colorWeight = 0.05
		visualKeyWeight = 0.95

		return (color * colorWeight) + (visualKey * visualKeyWeight)

	def combineResults(self, color, visualKey, limit = 20):
		keys = color.keys()
		print "METALLICA"
		if color.keys() == visualKey.keys():
			print "HALLE"

		color = np.asarray(color.values())
		visualKey = np.asarray(visualKey.values())

		newVals = self.weightResults(color, visualKey)

		weightedScores = dict(zip(keys, newVals.tolist()))

		rankedScores = sorted([(v, k) for (k, v) in weightedScores.items()])

		print rankedScores[:limit]
		return rankedScores[:limit]

	# def chi2_distance(self, histA, histB, eps = 1e-10):
	# 	histA = np.asarray(histA)
	# 	histB = np.asarray(histB)
	# 	# # compute the chi-squared distance
	# 	# d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
	# 	# 	for (a, b) in zip(histA, histB)])

	# 	# # return the chi-squared distance
	# 	# return d
	# 	# print type(histA), type(histB)
	# 	return dist.chebyshev(histA, histB)
	# 	# return cv2.compareHist(histA, histB, cv2.cv.CV_COMP_CORREL)
