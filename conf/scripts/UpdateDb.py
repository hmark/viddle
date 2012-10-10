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

#db = DBConnection().get_db()
#reset(db)