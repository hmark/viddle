import pymongo
import os

class DBConnection:

	def __init__(self):
		f = open("../db.conf", "r")
		dbCon = f.readline().strip()
		connection = pymongo.Connection(dbCon)
		self.db = connection.db_viddle

	def get_db(self):
		return self.db

def reset(db):
	db.links.remove()

def create_field(db):
	db.links.update({"_id":link["_id"]}, {"$set" : {"date" : date, "time" : time}})

def remove_field(db):
	db.links.update({"_id":link["_id"]}, {"$unset" : {"datetime" : 1}}, False, True)

def update_player_for_video(db):
	import re

	results = db.links.find({"video":{"$exists": "true"}}, {"video":1})
	print(results.count())
	for result in results:
		print(result["_id"], result["video"][0])

		if re.match(r"^http://i.sme.sk/datamm", result["video"][0]): 
			db.links.update({'_id': result["_id"]},{"$set" : {"player" : "sme.sk"}})
		elif re.match(r"^http://www.youtube.com/embed", result["video"][0]):
			db.links.update({'_id': result["_id"]},{"$set" : {"player" : "youtube.com"}})
		elif re.match(r"^http://embed.ted.com/talks", result["video"][0]):
			db.links.update({'_id': result["_id"]},{"$set" : {"player" : "ted.com"}})
		elif re.match(r"^http://video.ted.com", result["video"][0]):
			db.links.update({'_id': result["_id"]},{"$set" : {"player" : "ted.com(old)"}})
	
def get_players(db):
	results = db.links.find({"video":{"$exists": "true"}})
	for result in results:
		print(result["video"][0])
		print(result["player"])

db = DBConnection().get_db()
#get_players(db)