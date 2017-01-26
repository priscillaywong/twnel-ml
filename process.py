import pymongo
import datetime
import pprint
import io
import csv


from pymongo import MongoClient
client = MongoClient()
db = client.twnel

messages = db.messages
conversations = db.conversations
companies = db.companies

mcount = messages.count()
ccount = conversations.count()
compcount = companies.count()

company_list = []
start_date = 1458777600000.0
#Milliseconds since 3/24/2016 00:00:00 GMT

print ("Number of messages: ", mcount)
print ("Number of conversations: ", ccount)
count = 1
number = 0

### Generate list company_list of all companies
file = open("companies.csv", "w")

for c in companies.find():
	if ("id" in c):
		name = "" + c["id"] + "@x.twnel.net"
		file.write(name)
		file.write(" " + str(number) + "\n")
		company_list.append(name)

file.close()

fmessages = csv.writer(open("filtered_messages.csv", "w", encoding='utf8'))
fmessages.writerow(['to', 'from', 'message', 'company', 'customer', 'time'])


for m in messages.find():

	count += 1
	if (count % 100000 == 0):
		print ("Progress:", 100.0 * count / mcount, "%")

	### Date filter
	date = m["created_at"]
	sdate=""
	if isinstance(date, float):   
		sdate=str(int(date/1000))
		if (date < start_date):
		      continue
	if isinstance(date, datetime.datetime):
     		sdate=str(int(float(date.strftime("%s"))))
     		if (1000 * float(date.strftime("%s")) < start_date):
		      continue

	### Message type filter
	content_type = m["content_type"]
	if (content_type != "text/plain" and content_type != "session/start" and content_type != "session/end"):
		continue

	### Broadcast filter
	if (m["isBroadcast"]):
		continue

	### write to csv if message is between a company and a customer
	body=m["body"]
	name_to = m["to"]
	name_from = m["from"]
	if body is None or name_to is None or name_from is None:
     		continue

	### stops after X messages
	limit=100
	if number>=limit:
		break

	### makes sure that message is between a company and a customer
	if isinstance(name_to,str):
		if isinstance(name_from,str):
		      if (name_to in company_list and "+" in name_from):
		           #fmessages.write(name_to+','+name_from+','+body+','+name_to+','+name_from+','+sdate+'\n')
		           fmessages.writerow([name_to,name_from,body,name_to,name_from,sdate])
		           number += 1
		      if (name_from in company_list and "+" in name_to):
		           number += 1	
		           #fmessages.write(name_to+','+name_from+','+body+','+name_from+','+name_to+','+sdate+'\n')
		           fmessages.writerow([name_to,name_from,body,name_from,name_to,sdate])
		if isinstance(name_from,list):
		      if (name_to in company_list and "+" in name_from[0]):
		           number += 1	
		           #fmessages.write(name_to+','+name_from[0]+','+body+','+name_to+','+name_from[0]+','+sdate+'\n')
		           fmessages.writerow([name_to,name_from[0],body,name_to,name_from[0],sdate])
		      if (name_from[0] in company_list and "+" in name_to):
		           number += 1	
		           #fmessages.write(name_to+','+name_from[0]+','+body+','+name_from[0]+','+name_to+','+sdate+'\n')
		           fmessages.writerow([name_to,name_from[0],body,name_from[0],name_to,sdate])
	if isinstance(name_to,list):
		if isinstance(name_from,str):
		      if (name_to[0] in company_list and "+" in name_from):
		           number += 1	
		           #fmessages.write(name_to[0]+','+name_from+','+body+','+name_to[0]+','+name_from+','+sdate+'\n')
		           fmessages.writerow([name_to[0],name_from,body,name_to[0],name_from,sdate])
		      if (name_from in company_list and "+" in name_to[0]):
		           number += 1	
		           #fmessages.write(name_to[0]+','+name_from+','+body+','+name_from+','+name_to[0]+','+sdate+'\n')
		           fmessages.writerow([name_to[0],name_from,body,name_to[0],name_from,sdate])
		if isinstance(name_from,list):
		      if (name_to[0] in company_list and "+" in name_from[0]):
		           number += 1	
		           #fmessages.write(name_to[0]+','+name_from[0]+','+body+','+name_to[0]+','+name_from[0]+','+sdate+'\n')
		           fmessages.writerow([name_to[0],name_from[0],body,name_to[0],name_from[0],sdate])
		      if (name_from[0] in company_list and "+" in name_to):
		           number += 1	
		           #fmessages.write(name_to[0]+','+name_from[0]+','+body+','+name_from[0]+','+name_to[0]+','+sdate+'\n')            
		           fmessages.writerow([name_to[0],name_from[0],body,name_from[0],name_to[0],sdate])

print (number)


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


























