import nltk
from nltk.stem.porter import *
import sys
import codecs
import collections

def main():

	infile  = sys.argv[1]
	outfile = sys.argv[2]
	out = open(outfile, 'w')

	images = {}

	stemmer = PorterStemmer()

	print "Tokenizing file..."
	with open(infile, 'r') as f:
		for line in f:
			tokens = nltk.word_tokenize(line)
			for token in tokens:
				if ".jpg" in token:
					img_name = token
					images[img_name] = []
					tokens.remove(img_name)
			images[img_name] = tokens


	for key in images:
		images[key] = [stemmer.stem(tag) for tag in images[key]]
	
	# WRITING TOKENIZED FILE 
	out.write("TOKENIZED FILE" + "\n")	
	for key in images:
		out.write(key + ": ")
		for tag in images[key]:
			out.write(tag + ", ")
		out.write("\n\n")

	print "Tokenized file written in \"" + outfile + "\""

	all_tags = []
	for key in images:
		for tag in images[key]:
			all_tags.append(tag)

	print "Inverted indexing the files..."
	inverted = {}
	files = []
	for tag in all_tags:
		inverted[tag] = []
		for key in images:
			if tag in images[key]:
				inverted[tag].append(key)

	print "Inverted indexed files written in \"" + outfile + "\""			
	# WRITING INVERTED FILE
	out.write("INVERTED INDEXED " + "\n")			
	for key in inverted:
		out.write(key + ": " + str(inverted[key]) + "\n")

	print "... done"
		
main()
