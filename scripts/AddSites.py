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
db.sites.remove()

print("Parsing new sites from config file...")
sites = []
regex = []
crawlers = []
for site in open("../vidcr/conf/sites.conf", "r"):	
	data = site.strip().split()
	sites.append(data[0])
	regex.append(data[1])
	crawlers.append(data[2])

for i in range(len(sites)):
	print("Adding site", sites[i], "with regex:", regex[i], "and crawler", crawlers[i])
	db.sites.insert({"site": sites[i], "regex":regex[i], "crawler": crawlers[i]});

print("Script succesfully terminated.");