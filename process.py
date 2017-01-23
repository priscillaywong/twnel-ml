import pymongo
import datetime
import pprint


from pymongo import MongoClient
client = MongoClient()
db = client.twnel

messages = db.messages
conversations = db.conversations
mcount = messages.count()
ccount = conversations.count()

companies = []
start_date = 1458777600000.0
#Milliseconds since 3/24/2016 00:00:00 GMT

print "Number of messages: ", mcount
print "Number of conversations: ", ccount
count = 1
number = 0

for m in messages.find():

	count += 1
	if (count % 100000 == 0):
		print "Progress:", 100.0 * count / mcount, "%"

	### Date filter
	date = m["created_at"]
	if isinstance(date, float) and (date < start_date):
		continue
	if isinstance(date, datetime.datetime) and (1000 * float(date.strftime("%s")) < start_date):
		continue

	### Message type filter
	content_type = m["content_type"]
	if (content_type != "text/plain" and content_type != "session/start" and content_type != "session/end"):
		continue

	### Broadcast filter
	if (m["isBroadcast"]):
		continue

	number += 1

print number

'''
for m in messages.find():

	print "Message #:", count
	#print "ID:", m["_id"]
	name_to = m["to"]
	name_from = m["from"]
	print "To:", name_to
	print "From:", name_from
	if ("+" in name_to or "+" in name_to[0]):
		print "To a customer"
	elif (name_to not in companies):
		companies.append(name_to)
	if ("+" in name_from or "+" in name_from[0]):
		print "From a customer"
	elif (name_from not in companies):
		companies.append(name_from)
	count += 1
	if (count % 93500 == 0):
		print (100.0 * count / mcount), "%", "done"
		print companies
		print len(companies)
		break
'''


























