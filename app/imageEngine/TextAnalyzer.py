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
    def __init__(self, query, infile, outfile):
        self.query   = query
        self.infile  = infile
        self.outfile = outfile

    def run(self):
        self.process(self.infile)
        query = self.query
        self.print_result(process_query(query), self.outfile)
        print "\n\nSearch completed"

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

        # FIRST QUERY FILTER: STOP WORDS
        stop = stopwords.words('english')
        stop = [word.encode('ascii', 'ignore') for word in stop]
        processed_query = [word for word in query.split() if word not in stop]

        # SECOND QUERY FILTER: STEMMING
        processed_query = [stemmer.stem(word).encode('ascii', 'ignore') for word in processed_query]

        return processed_query

    def print_result(self, query, outfile):

        out = open(outfile, 'w')

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

        for key,value in rankings:
            out.write(str (key) + "\n")
            out.write(str (value) + "\n\n")

    def cosine_sim(self, query, document):
        vect = TfidfVectorizer(min_df=1)

        str_query = str(query)
        str_doc   = str(document)

        tfidf = vect.fit_transform([str_query, str_doc])
        return ((tfidf*tfidf.T).A)[0,1]
