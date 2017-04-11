import gensim, logging
import csv
import re
import numpy
import pickle
import pandas as pd
from bs4 import BeautifulSoup
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = gensim.models.Word2Vec.load("mymodel")

def save_obj(obj, name):
	with open("" + name + ".pkl", "wb") as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
	with open("" + name + ".pkl", "rb") as f:
		return pickle.load(f)

def getNull():
	return numpy.zeros_like(model["SESSION_END"])

def isNull(vector):
	for x in range(100):
		if (vector[x] != 0):
			return False
	return True

print "Loading the sentences"
sentences = load_obj("sentences")

csvreader = csv.reader(open("messages.csv", "rb"))
sentence_vectors = []
index_to_vector = {}
index_to_sentence = {}

outside_counter = 0

for sentence in sentences:

	#Mapping index to the sentence
	index_to_sentence[outside_counter] = sentence

	count = 0

	vector = getNull()

	for word in sentence:
		if (word in model):
			vector += model[word]
			count += 1

	# No word in this sentence is recognized by our model
	if isNull(vector):
		index_to_vector[outside_counter] = vector
		sentence_vectors.append(vector)
		continue

	# There is at least one word recognized by our model in this sentence
	for x in range(100):
		vector[x] = 1.0 * vector[x] / count

	index_to_vector[outside_counter] = vector
	sentence_vectors.append(vector)

	#print vector, "\n"

	outside_counter += 1
	if (outside_counter % 50000 == 0):
		print "Lines processed:", outside_counter

print "Saving index_to_vector dictionary"
save_obj(index_to_vector, "num_to_vector")

print "Saving index_to_sentence dictionary"
save_obj(index_to_sentence, "num_to_sentence")










