import pymongo

class DBConnection:

	def __init__(self):
		f = open("./conf/db.conf", "r")
		dbCon = f.readline().strip()
		connection = pymongo.Connection(dbCon)
		self.db = connection.db_viddle

	def get_db(self):
		return self.db
