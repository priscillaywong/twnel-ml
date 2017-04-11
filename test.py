import gensim, logging
import csv
import re
import numpy
import pickle
import math
import pandas as pd
from bs4 import BeautifulSoup
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = gensim.models.Word2Vec.load("mymodel")


def magnitude(vector):
	total = 0.0
	for entry in vector:
		total += entry * entry
	return math.sqrt(total)

def dotProduct(vector1, vector2):
	total = 0.0
	if (not len(vector1) == len(vector2)):
		return 0.0
	else:
		for index in range(len(vector1)):
			total += vector1[index] * vector2[index]
	return total

def similarity(vector1, vector2):
	total = 0.0
	if (not len(vector1) == len(vector2)):
		return 0.0
	else:
		a = magnitude(vector1)
		b = magnitude(vector2)
		if (a == 0 or b == 0):
			return 0
		else:
			return dotProduct(vector1, vector2) / (a * b)

def save_obj(obj, name):
	with open("" + name + ".pkl", "wb") as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
	with open("" + name + ".pkl", "rb") as f:
		return pickle.load(f)

def getNull():
	return numpy.zeros_like(model["SESSION_END"])

sentence_vectors = []
outside_counter = 0

print "Loading index-to-sentence dictionary"
sentence_dict = load_obj("num_to_sentence")
print "Loading index-to-vector dictionary"
vector_dict = load_obj("num_to_vector")

print "Size of index-to-sentence dictionary:", len(sentence_dict)
print "Size of index-to-vector dictinoary:", len(vector_dict)

print sentence_dict[1]
print vector_dict[1]
print "Type:", type(vector_dict[1])

sentence = raw_input('Enter a question: ')

words = sentence.lower().split()
length = len(words)
count = 0

vector = getNull()

for word in words:
	if word in model:
		vector += model[word]
		count += 1

if (count == 0):
	print "Sentence not found"
else:
	for x in range(100):
		vector[x] = 1.0 * vector[x] / count
	first_index = -1
	second_index = -1
	third_index = -1
	first_max = 0.0
	second_max = 0.0
	third_max = 0.0
	for index in range(len(vector_dict)):
		closeness = similarity(vector_dict[index], vector)
		smallest = min(first_max, min(second_max, third_max))
		if (closeness > smallest):
			if (smallest == first_max):
				first_index = index
				first_max = closeness
			elif (smallest == second_max):
				second_index = index
				second_max = closeness
			else:
				third_index = index
				third_max = closeness

	print "\nFirst possible response:", sentence_dict[first_index + 1]
	print "\nSecond possible response:", sentence_dict[second_index + 1]
	print "\nThird possible response:", sentence_dict[third_index + 1]


#NOTE: CONSIDER HAVING A THRESHOLD








