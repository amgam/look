# import the necessary packages
import numpy as np
import pickle
import cv2
import numpy as np
from scipy.spatial import distance as dist

 
class ImageComparator:
	def __init__(self, indexPath):
		# store our index path
		self.indexPath = indexPath

	def compare(self, queryFeatures, limit = 10):
		# initialize our dictionary of results
		results = {}

		queryDict = pickle.load(open(self.indexPath, "rb"))

		for imgName, features in queryDict.iteritems():
			distance = self.euclideanDistance(queryFeatures, features)

			results[imgName] = distance

		results = sorted([(v, k) for (k, v) in results.items()])

		return results
		# return results

	def distIntersection(self, queryHist, otherHist):
		queryHist = np.asarray(queryHist)
		otherHist = np.asarray(otherHist)

		return cv2.compareHist(queryHist, otherHist, cv2.cv.CV_COMP_INTERSECT)

	def euclideanDistance(self, queryHist, otherHist):
		queryHist = np.asarray(queryHist)
		otherHist = np.asarray(otherHist)

		return np.linalg.norm(queryHist-otherHist)
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
