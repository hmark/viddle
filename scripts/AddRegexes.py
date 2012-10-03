import pymongo
import os

class DBConnection:

	def __init__(self):
		f = open(os.path.dirname(__file__) + "/../vidcr/conf/db.conf", "r")
		dbCon = f.readline().strip()
		connection = pymongo.Connection(dbCon)
		self.db = connection.db_viddle

	def get_db(self):
		return self.db

db = DBConnection().get_db()

print("Removing all sites from db...")
db.regexes.remove()

print("Parsing regexes from config file...")
tags = []
regexes = []
for line in open("../vidcr/conf/regex.conf", "r"):
	data = line.strip().split()
	tags.append(data[0])
	regexes.append(data[1])

for i in range(len(tags)):
	print("Adding tag", tags[i], "with regex:", regexes[i])
	db.regexes.insert({"tag": tags[i], "regex":regexes[i]})

print("Script succesfully terminated.");