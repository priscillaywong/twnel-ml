import pymongo
import datetime
import pprint
import io
import csv

reader = open("filtered_messages.csv", "r")
writer = csv.writer(open("messages.csv", "w"))

count = 0

for line in reader:
	count += 1

	if (count == 1):
		continue

	if (count % 50000 == 0):
		print "Progress:", count, "lines processed."

	words = line.split(",")
	if (len(words) != 6):
		continue
	company = words[0]
	sender = words[3]
	message = words[5][:-2]
	if (company == sender):
		writer.writerow(["Agent", message])
	else:
		writer.writerow(["Customer", message])