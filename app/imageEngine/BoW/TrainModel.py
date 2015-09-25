#!/usr/local/bin/python2.7

import argparse as ap
import cv2
import imutils 
import numpy as np
import os
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from scipy.cluster.vq import *
from sklearn.preprocessing import StandardScaler
import glob
import simplejson

class TrainModel:
    def listdir_nohidden(self, path):
        return glob.glob(os.path.join(path, '*'))

    def __init__(self, path, flag="def"):
        print "init"
        # Get the path of the training set
        # parser = ap.ArgumentParser()
        # parser.add_argument("-t", "--trainingSet", help="Path to Training Set", required="True")
        # args = vars(parser.parse_args())
        # Get the training classes names and store them in a list
        # print path
        #path to dict
        self.imgInfo =  "static/data/imgInfo.json"
        self.trainPath = path
        self.trainingNames = self.listdir_nohidden(self.trainPath)
        # Get all the path to the images and save them in a list
        # image_paths and the corresponding label in image_paths
        self.image_paths = []
        self.image_classes = []
        self.class_id = 0
        # print "len", len(self.trainingNames)
        if flag == "analyze":
            training_name = self.trainingNames
            class_path = training_name
            self.image_paths+=class_path
            self.image_classes+=[self.class_id]*len(class_path)
            self.class_id+=1
        elif flag == "def":
            for training_name in self.trainingNames:
                dir = training_name
                class_path = imutils.imlist(dir)
                self.image_paths+=class_path
                self.image_classes+=[self.class_id]*len(class_path)
                self.class_id+=1
           
        # print "IMAGE:", self.image_paths
        # print self.trainingNames
        # print self.test

    def extractName(self, input):
        # print input
        return input.split("/")[3]

    def train(self):
        print "training..."
        # Create feature extraction and keypoint detector objects

        fea_det = cv2.FeatureDetector_create("SIFT")
        des_ext = cv2.DescriptorExtractor_create("SIFT")

        # List where all the descriptors are stored
        des_list = []

        for image_path in self.image_paths:
            im = cv2.imread(image_path)
            kpts = fea_det.detect(im)
            kpts, des = des_ext.compute(im, kpts)
            des_list.append((image_path, des))   

        # Stack all the descriptors vertically in a numpy array
        descriptors = des_list[0][1]

        for image_path, descriptor in des_list[1:]:
            descriptors = np.vstack((descriptors, descriptor))  

        # Perform k-means clustering
        k = 100
        voc, variance = kmeans(descriptors, k, 1) 

        # Calculate the histogram of features
        im_features = np.zeros((len(self.image_paths), k), "float32")

        for i in xrange(len(self.image_paths)):
            words, distance = vq(des_list[i][1],voc)

            for w in words:
                im_features[i][w] += 1

        # Perform Tf-Idf vectorization
        nbr_occurences = np.sum( (im_features > 0) * 1, axis = 0)
        idf = np.array(np.log((1.0*len(self.image_paths)+1) / (1.0*nbr_occurences + 1)), 'float32')

        # Scaling the words
        stdSlr = StandardScaler().fit(im_features)
        im_features = stdSlr.transform(im_features)
        
        #extract image names
        imgNames = map(self.extractName, self.image_paths)

        with open(self.imgInfo) as imgInfo:
            imgDict = simplejson.load(imgInfo)

        for idx, name in enumerate(imgNames):
            imgDict[name]["visualHist"] = im_features[idx].tolist()

        with open(self.imgInfo, 'w') as fp:
            simplejson.dump(imgDict, fp) 

        # Train the Linear SVM
        clf = LinearSVC()
        clf.fit(im_features, np.array(self.image_classes))

        # Save the SVM
        joblib.dump((clf, self.trainingNames, stdSlr, k, voc), "static/data/bof.pkl", compress=3)
        print "trained." 

    def uploadAnalysis(self):
        clf, classes_names, stdSlr, k, voc = joblib.load("static/data/bof.pkl")

        fea_det = cv2.FeatureDetector_create("SIFT")
        des_ext = cv2.DescriptorExtractor_create("SIFT")

        # List where all the descriptors are stored
        des_list = []

        for image_path in self.image_paths:
            im = cv2.imread(image_path)
            # print "im:", im
            kpts = fea_det.detect(im)
            kpts, des = des_ext.compute(im, kpts)
            des_list.append((image_path, des))   

        # Stack all the descriptors vertically in a numpy array
        descriptors = des_list[0][1]

        for image_path, descriptor in des_list[0:]:
            descriptors = np.vstack((descriptors, descriptor))  

        # Perform k-means clustering
        # k = 100
        # voc, variance = kmeans(descriptors, k, 1) 
        # Calculate the histogram of features
        test_features = np.zeros((len(self.image_paths), k), "float32")

        # print "HERE:", self.image_paths

        for i in xrange(len(self.image_paths)):
            words, distance = vq(des_list[i][1],voc)

            for w in words:
                test_features[i][w] += 1

        # Perform Tf-Idf vectorization
        nbr_occurences = np.sum( (test_features > 0) * 1, axis = 0)
        idf = np.array(np.log((1.0*len(self.image_paths)+1) / (1.0*nbr_occurences + 1)), 'float32')

        # print im_features
        # Scaling the words
        # stdSlr = StandardScaler().fit(im_features)
        test_features = stdSlr.transform(test_features)
        print "imfeat: ", [classes_names[i] for i in clf.predict(test_features)]
        return test_features
        #extract image names
        # imgNames = map(self.extractName, self.image_paths)

        # with open(self.imgInfo) as imgInfo:
        #     imgDict = simplejson.load(imgInfo)

        # for idx, name in enumerate(imgNames):
        #     imgDict[name]["visualHist"] = im_features[idx].tolist()

        # with open(self.imgInfo, 'w') as fp:
        #     simplejson.dump(imgDict, fp) 

        # # Train the Linear SVM
        # clf = LinearSVC()
        # clf.fit(im_features, np.array(self.image_classes))

        # # Save the SVM
        # joblib.dump((clf, self.trainingNames, stdSlr, k, voc), os.getcwd() + "/static/data/bof.pkl", compress=3)
        print "analysed." 


        
