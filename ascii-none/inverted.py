import sys
import operator
import unicodedata
import itertools
import nltk
from nltk.stem.porter import *
from nltk.corpus import stopwords
from nltk.text import TextCollection
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer

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

	all_tags = []
	for key in images:
		for tag in images[key]:
			all_tags.append(tag)

	inverted = {}
	files = []
	for tag in all_tags:
		inverted[tag] = []
		for key in images:
			if tag in images[key]:
				inverted[tag].append(key)
			
	# WRITING INVERTED FILE
	out.write("INVERTED INDEXED " + "\n")			
	for key in inverted:
		out.write(key + ": " + str(inverted[key]) + "\n")

	out.write("\n\n" "IDF" + "\n")		
	col = nltk.TextCollection(images.values())
	for word in inverted.keys():
		out.write(word + ": " + str(col.idf(word)) + "\n") 

	query = raw_input('Search: ')

	# FIRST QUERY FILTER: STOP WORDS
	stop = stopwords.words('english')
	query_keywords = [word for word in query.split() if word not in stop]
	# SECOND QUERY FILTER: STEMMING
	query_keywords = [stemmer.stem(word).encode('ascii', 'ignore') for word in query_keywords]

	# FIRST RESULT FILTER
	# if query word is in hashtag, then return document
	relevant = []
	for keyword in query_keywords:
		for key in inverted:
			if keyword in key:
				relevant.append(inverted[key])

	# merge lists in relevant list
	relevant = list(itertools.chain(*relevant))
	# set dictionary keys
	unordered_ranking = {}
	for filename in relevant:
		unordered_ranking[filename] = 0

	# SECOND RESULT FILTER
	# CALC TF-IDF FOR RANKING OF SEARCH RESULTS
	for filename in unordered_ranking:
		tags = images[filename]
		value = cosine_sim(query_keywords, tags)
		unordered_ranking[filename] = value

	rankings = sorted(unordered_ranking.items(), key=operator.itemgetter(1), reverse=True)

	for key,value in rankings:
		print key
		print value

def cosine_sim(query, document):
	vect = TfidfVectorizer(min_df=1)

	str_query = str(query)
	str_doc   = str(document)

	tfidf = vect.fit_transform([str_query, str_doc])
	return ((tfidf*tfidf.T).A)[0,1] 

main()