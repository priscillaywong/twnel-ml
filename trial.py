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

def getNull():
	return numpy.zeros_like(model["SESSION_END"])

sentence = raw_input('Enter a question: ')


print type(sentence)

words = sentence.lower().split()

print len(words)
print words

count = 0

vector = getNull()
for word in words:
	if word in model:
		vector += model[word]
		count += 1

if (count == 0):
	print "Sentence not found"