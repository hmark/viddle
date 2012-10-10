"""This module serves as database connector.
"""

import pymongo
import os

class DBConnection:
	"""Mongo database connector.
	"""

	def __init__(self):
		"""Load db access data from file and create pymongo db connection.
		"""

		f = open(os.path.dirname(__file__) + "/../conf/db.conf", "r")
		dbCon = f.readline().strip()
		connection = pymongo.Connection(dbCon)
		self.db = connection.db_viddle

	def get_db(self):
		"""Returns pymongo database object.
		"""

		return self.db
