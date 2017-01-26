import pymongo
import datetime
import pprint


from pymongo import MongoClient
client = MongoClient()
db = client.twnel

companies = db.companies
count = companies.count()

company_list = []
number = 0

file = open("companies.csv", "w")

for c in companies.find():
	if ("id" in c):
		name = "" + c["id"] + "@x.twnel.net"
		file.write(name)
		file.write(" " + str(number) + "\n")
		number += 1

file.close()

print ("There are", count, "companies in this list.")
print ("There are", number, "company emails.")