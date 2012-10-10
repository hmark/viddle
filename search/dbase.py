import pymongo
import os

class DBConnection:

	def __init__(self):
		f = open(os.path.dirname(__file__) + "/../conf/db.conf", "r")
		dbCon = f.readline().strip()
		connection = pymongo.Connection(dbCon)
		self.db = connection.db_viddle

	def get_db(self):
		return self.db
