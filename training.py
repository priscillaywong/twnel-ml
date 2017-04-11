# import modules & set up logging
import gensim, logging
import csv
import re
import numpy
import pickle
import math
import pandas as pd
from bs4 import BeautifulSoup
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def save_obj(obj, name):
	with open("" + name + ".pkl", "wb") as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
	with open("" + name + ".pkl", "rb") as f:
		return pickle.load(f)

csvreader = csv.reader(open("messages.csv", "rb"))
sentences = []
count = 0

isCustomer = None
currentMessage = []

for row in csvreader:

	count += 1
	if (count % 100000 == 0):
		print count, "lines read"
	if (count == 100000000):
		break

	sender = row[0]
	message = row[1]
	a_to_z = re.sub("[^a-zA-Z]", "", message)
	words = a_to_z.lower().split()

	if (message == "SESSION_END"):
		sentences.append(currentMessage)
		sentences.append(["SESSION_END"])
		currentMessage = []
		isCustomer = None
		continue

	#Continuation
	if (isCustomer != None):
		if ((not isCustomer and sender == "Customer") or (isCustomer and sender == "Agent")):
			sentences.append(currentMessage)
			currentMessage = []
		for w in words:
			currentMessage.append(w)

	#The first line of a conversation
	if (isCustomer == None):
		if (sender == "Customer"):
			isCustomer = True
		else:
			isCustomer = False
		for w in words:
			currentMessage.append(w)

	isCustomer = (sender == "Customer")

model = gensim.models.Word2Vec(sentences, min_count=10, size=100, iter=10)

print "Training complete!"
print "Similarity between \"thanks\" and \"please\":", model.similarity("thanks", "please")
model.save('mymodel')

print "Saving the list of sentences"
save_obj(sentences, "sentences")

for x in range(10):
	print sentences[x]















