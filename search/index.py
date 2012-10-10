"""This module serves as whoosh index engine mediator.
"""

import pymongo
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.index import create_in, open_dir
import os.path

class Whoosh:
	"""Reads and writes searching data to index engine.
	Check detailed whoosh index specification at http://packages.python.org/Whoosh/
	"""

	def __init__(self):
		"""Constructor.
		"""
		self.init()
		#self.load()

	def init(self):
		"""Index and writer object initialization.
		If index does not exist then create new in the specified path.
		"""

		pathname = os.path.dirname(__file__) + "/../data/index"
		if not os.path.exists(pathname): # create new index if it does not exist yet
			create_index(pathname)
			
		self.index = open_dir(pathname)
		self.writer = self.index.writer()

	#def load(self):
	#	connection = pymongo.Connection("mongodb://viddle_user:viddle_user21@ds037647-a.mongolab.com:37647/db_viddle")
	#	db = connection.db_viddle

		#for doc in db.links.find({"video":{"$exists":"True"}}):
		#	print(doc)

	#	for doc in db.links.find({"video":{"$exists":"True"}}):
	#		texts_len = len(doc["texts"])
	#		titles_len = len(doc["title"])
	#		self.add_document(doc["url"], doc["video"], ''.join(doc["title"][0:titles_len]), ''.join(doc["title"][0:titles_len]), ''.join(doc["title"][0:titles_len]), ''.join(doc["texts"][0:texts_len]))

	#	self.commit()

	def create_index(self, path):
		"""Create new index with db schema:
		url (ID, stored, unique)
		video (ID, stored, unique)
		name (TEXT, stored)
		title (TEXT, stored, field_boost)
		body (vector, stored)

		:param path: Directory where the index will be created.
		"""

		schema = Schema(url=ID(stored=True, unique=True), video=ID(stored=True, unique=True), name=TEXT(stored=True), title=TEXT(stored=True, field_boost=5.0), body=TEXT(vector=True, stored=True))
		os.mkdir(path)
		self.index = create_in(path, schema)

	def add_document(self, url, video, name, title, body):
		"""Add new document to whoosh writer. Variables must be compatible with index schema.

		:param url: page URL
		:param video: video identificator
		:param name: full name (can contain words with special characters)
		:param title: extended name (can contain derived words)
		:param body: page text
		"""

		self.writer.add_document(url=url, video=video, name=name, title=title, body=body)

	#def remove_document(self): # USE ONLY IN SPECIAL CASES
	#	self.writer.delete_document(1)

	def commit(self):
		"""Commit all added documents from writer to index.
		"""

		self.writer.commit(optimize=True)

