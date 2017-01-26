import pymongo
import datetime
import pprint

class Chat:
	def __init__(self, message, sender, receiver, timestamp):
		self.m = message
		self.s = sender
		self.r = receiver
		self.t = timestamp
	def __str__(self):
		return "{" + self.m + "\n\tFrom: " + self.s + "\n\tTo: " + self.r + "\n\tTimestamp: " + str(self.t) + "\n}"

from pymongo import MongoClient
client = MongoClient()
db = client.twnel

messages = db.messages
conversations = db.conversations
mcount = messages.count()
ccount = conversations.count()

reader = open('companies.csv', 'r')

### Creating the hash table
c_to_int = {}
int_to_c = {}
for line in reader:
	new_line = line.split(" ")
	company = new_line[0]
	num = new_line[1][:-1]
	c_to_int[company] = int(num)
	int_to_c[num] = company

###creating the messages table
database = []
for x in range(793):
	database.append([])

count = 0
start_date = 1458777600000.0
#Milliseconds since 3/24/2016 00:00:00 GMT

for m in messages.find():

	count += 1
	if (count % 10000 == 0):
		break

	### Date filter
	### Timestamp is in milliseconds
	date = m["created_at"]
	if isinstance(date, float) and (date < start_date):
		continue
	if isinstance(date, datetime.datetime) and (1000 * float(date.strftime("%s")) < start_date):
		continue
	if isinstance(date, datetime.datetime):
		date = float(date.strftime("%s")) * 1000.0

	### Message type filter
	content_type = m["content_type"]
	if (content_type != "text/plain" and content_type != "session/start" and content_type != "session/end"):
		continue

	### Broadcast filter
	if (m["isBroadcast"]):
		continue

	sender = m["from"]
	receiver = m["to"][0]
	body = m["body"]

	print ("Sender:", sender)
	print ("Receiver:", receiver)

	if (sender == None or receiver == None or body == None or date == None):
		continue


	text = Chat(body, sender, receiver, date)
	if (sender in c_to_int):
		database[c_to_int[sender]].append(text)
	elif (receiver in c_to_int):
		database[c_to_int[receiver]].append(text)

for chat in database[1]:
	print (chat.__str__())




