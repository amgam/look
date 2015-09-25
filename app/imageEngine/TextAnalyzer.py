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

class TextAnalyzer:
    def __init__(self, queryfile, infile):
        self.queryfile   = queryfile
        self.infile  = infile

    def run(self):
        self.process(self.infile)
        queryfile = self.queryfile
        processed_query = process_query(queryfile)
        final_result = {}
        for key in processed_query:
            final_result[key] = get_result(processed_query[key])

    def process(self, infile):
        global tokenized_file 
        tokenized_file = self.tokenize(infile)
        global inverted_file 
        inverted_file = self.inverted_index(tokenized_file)

    def tokenize(self, infile):

        images = {}

        global stemmer 
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
                images[key] = [stemmer.stem(tag).encode('ascii', 'ignore') for tag in images[key]]
            except UnicodeDecodeError:
                continue
        
        return images

    def inverted_index(self, tokenized_file):
        all_tags = []
        for key in tokenized_file:
            for tag in tokenized_file[key]:
                all_tags.append(tag)

        inverted = {}
        for tag in all_tags:
            inverted[tag] = []
            for key in tokenized_file:
                if tag in tokenized_file[key]:
                    inverted[tag].append(key)

        return inverted

    def process_query(self, query):

        query_images = {}

        #process query
        with open(query, 'r') as f:
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
                        query_images[img_name] = []
                        tokens.remove(img_name)
                query_images[img_name] = tokens


        for key in query_images:
            try:
                query_images[key] = [stemmer.stem(tag).encode('ascii', 'ignore') for tag in query_images[key]]
            except UnicodeDecodeError:
                print "UDE"

        return query_images

    def get_result(self, query):

        # FIRST RESULT FILTER
        # if query word is in hashtag, then return document
        relevant = []
        for keyword in query:
            for key in inverted_file:
                if keyword in key:
                    relevant.append(inverted_file[key])

        # merge lists in relevant list
        relevant = list(itertools.chain(*relevant))
        # set dictionary keys
        unordered_ranking = {}
        for filename in relevant:
            unordered_ranking[filename] = 0

        # SECOND RESULT FILTER
        # CALC TF-IDF FOR RANKING OF SEARCH RESULTS
        for filename in unordered_ranking:
            tags = tokenized_file[filename]
            value = self.cosine_sim(query, tags)
            unordered_ranking[filename] = value

        rankings = sorted(unordered_ranking.items(), key=operator.itemgetter(1), reverse=True)

        return rankings
        
    def cosine_sim(self, query, document):
        vect = TfidfVectorizer(min_df=1)

        str_query = str(query)
        str_doc   = str(document)

        tfidf = vect.fit_transform([str_query, str_doc])
        return ((tfidf*tfidf.T).A)[0,1]
