import pymongo
import datetime
import pprint
import io
import csv

from pymongo import MongoClient
client = MongoClient()
db = client.twnel

class Message:
	def __init__(self, company, customer, timestamp, sender, receiver, message):
		self.company = company
		self.customer = customer
		self.timestamp = timestamp
		self.sender = sender
		self.receiver = receiver
		self.message = message

	def display(self):
		output = ""
		output += "Company: " + self.company + "\n"
		output += "Customer: " + self.customer + "\n"
		output += "Timestamp: " + str(self.timestamp) + "\n"
		output += "\tFrom: " + self.sender + "\n"
		output += "\tTo: " + self.receiver + "\n"
		output += "\t\tMessage: " + self.message + "\n"
		print output

def change_text(text):
    return text.encode('utf-8')  # assuming the encoding is UTF-8

messages = db.messages
conversations = db.conversations
companies = db.companies

messages_count = messages.count()
conversations_count = conversations.count()
company_count = companies.count()

company_list = []
c_to_int = {}
int_to_c = {}
start_date = 1458777600000.0
#Milliseconds since 3/24/2016 00:00:00 GMT

print "Number of Messages: ", messages_count
print "Number of conversations: ", conversations_count

number = 0

# Generate list of all companies (company_list)
# Also generates the hash table, which is zero-indexed
file = open("companies.csv", "w")
for c in companies.find():
	if (c not in company_list and "id" in c):
		name = "" + c["id"] + "@x.twnel.net"
		c_to_int[name] = number
		int_to_c[number] = name
		file.write(name)
		file.write(" " + str(number) + "\n")
		number += 1
		company_list.append(name)
file.close()

print "There are", company_count, "companies in the database."
print "There are", number, "company emails in this list."

# Create the database of messages sorted by company
database = [[] for i in range(number)]

number_chats = 0
count = 0

fmessages = csv.writer(open("filtered_messages.csv", "w"))
fmessages.writerow(["Company", "Customer", "Timestamp", "From", "To", "Body"])

for message in messages.find():

	# Keeps track of progress of the program
	count += 1
	if (count % 100000 == 0):
		print "Progress:", count, "out of", messages_count

	# Date filter
	# Timestamp is a float
	date = message["created_at"]
	timestamp = -1
	if isinstance(date, float):
		timestamp = 1.0 * date / 1000.0
		if (date < start_date):
			continue
	elif isinstance(date, datetime.datetime):
		timestamp = float(date.strftime("%s"))
		if (1000 * float(date.strftime("%s")) < start_date):
			continue

	# Message type filter
	content_type = message["content_type"]
	if (content_type != "text/plain" and content_type != "session/start" and content_type != "session/end"):
		continue

	# Broadcast filter
	if (message["isBroadcast"]):
		continue

	# Write to csv if message is between a company and a customer
	body = message["body"]
	name_to = message["to"]
	name_from = message["from"]
	company = ""
	customer = ""
	if (content_type == "session/end"):
		body = "SESSION_END"
		
	if (body is None or name_to is None or name_from is None):
		continue

	skip = []
	#english login code
	skip.append("your Twnel login code. This code will expire")
	#spanish login code
	skip.append("minutos. Por favor, no responda este mensaje.")
	#english pending messages
	skip.append("now. Log in as agent using")
	skip.append("waiting for a response from your company right now.")
	skip.append("waiting to be helped.")
	skip.append("This could be the face")
	#spanish pending messages
	skip.append("conversaciones pendientes por atender. Ingrese como agente usando")
	skip.append("En este momento hay una")
	skip.append("esperando una respuesta de su empresa en este momento")


	move_on = False
	for s in skip:
		if (s in body):
			move_on = True
			break

	if (move_on):
		continue

	# Stops after X messages
	'''
	limit = 1000
	if count >= limit:
		break
	'''

	# Makes sure that message is between a company and a customer
	if isinstance(name_to, unicode):
		if isinstance(name_from, unicode):
			if (name_to in company_list and "+" in name_from):
				#fmessages.writerow([name_to,name_from,body,name_to,name_from,sdate])
				company = str(name_to)
				customer = str(name_from)
				name_to = company
				name_from = customer
				number_chats += 1
			elif (name_from in company_list and "+" in name_to):
				#fmessages.writerow([name_to,name_from,body,name_from,name_to,sdate])
				company = str(name_from)
				customer = str(name_to)
				name_from = company
				name_to = customer
				number_chats += 1
		elif isinstance(name_from, list):
			if (name_to in company_list and "+" in name_from[0]):
				#fmessages.writerow([name_to,name_from[0],body,name_to,name_from[0],sdate])
				company = str(name_to)
				customer = str(name_from[0])
				name_to = company
				name_from = customer
				number_chats += 1
			elif (name_from[0] in company_list and "+" in name_to):
				#fmessages.writerow([name_to,name_from[0],body,name_from[0],name_to,sdate])
				company = str(name_from[0])
				customer = str(name_to)
				name_from = company
				name_to = customer
				number_chats += 1
	elif isinstance(name_to, list):
		if isinstance(name_from, unicode):
			if (name_to[0] in company_list and "+" in name_from):
				#fmessages.writerow([name_to[0],name_from,body,name_to[0],name_from,sdate])
				company = str(name_to[0])
				customer = str(name_from)
				name_to = company
				name_from = customer
				number_chats += 1
			elif (name_from in company_list and "+" in name_to[0]):
				#fmessages.writerow([name_to[0],name_from,body,name_to[0],name_from,sdate])
				company = str(name_from)
				customer = str(name_to[0])
				name_from = company
				name_to = customer
				number_chats += 1
		elif isinstance(name_from, list):
			if (name_to[0] in company_list and "+" in name_from[0]):
				#fmessages.writerow([name_to[0],name_from[0],body,name_to[0],name_from[0],sdate])
				company = str(name_to[0])
				customer = str(name_from[0])
				name_to = company
				name_from = customer
				number_chats += 1
			elif (name_from[0] in company_list and "+" in name_to):
				#fmessages.writerow([name_to[0],name_from[0],body,name_from[0],name_to[0],sdate])
				company = str(name_from[0])
				customer = str(name_to)
				name_from = company
				name_to = customer
				number_chats += 1

	if (company == "" or customer == ""):
		continue
	
	chat = Message(company, customer, timestamp, name_from, name_to, body)
	database[c_to_int[company]].append(chat)

print "Processed chats:", number_chats
final_counter = 0

writer = csv.writer(open("messages.csv", "w"))

for l in database:
	l.sort(key=lambda x: x.timestamp)
	l.sort(key=lambda x: x.customer)
	for m in l:
		fmessages.writerow([m.company, m.customer, m.timestamp, m.sender, m.receiver, change_text(m.message)])
		if (m.company == m.sender):
			writer.writerow(["Agent", change_text(m.message)])
		elif (m.company == m.receiver):
			writer.writerow(["Customer", change_text(m.message)])

		final_counter += 1
		if (final_counter % 50000 == 0):
			print "Final Progress:", final_counter, "chats out of", number_chats, "processed chats."



