import sys
import unicodedata
import nltk
from nltk.stem.porter import *

def main():

	infile  = sys.argv[1]
	outfile = sys.argv[2]
	out = open(outfile, 'w')

	images = {}

	stemmer = PorterStemmer()

	with open(infile, 'r') as f:
		for line in f:
			tokens = line.split()
			for token in tokens:
				try:
					token.encode('utf-8')
					token.encode('ascii', 'ignore')
				except UnicodeDecodeError:
					tokens.remove(token)
				if ".jpg" in token:
					img_name = token
					images[img_name] = []
					tokens.remove(img_name)
			images[img_name] = tokens

	for key in images:
		try:
			images[key] = [stemmer.stem(tag) for tag in images[key]]
		except UnicodeDecodeError:
			print "UDE"

	# WRITING TOKENIZED FILE 
	out.write("TOKENIZED FILE" + "\n")
	for key in images:
		out.write(key + ": " + str(images[key]) + "\n\n")	
	# for key in images:
	# 	out.write(key + ": ")
	# 	for tag in images[key]:
	# 		out.write(tag + ", ")
	# 	out.write("\n\n")

main()