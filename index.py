import pymongo
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.index import create_in, open_dir
from whoosh.query import Every
import os.path

class Whoosh:

	def __init__(self):
		self.init()
		#self.load()

	def init(self):
		schema = Schema(url=ID(stored=True, unique=True), video=ID(stored=True, unique=True), title=TEXT(field_boost=5.0, stored=True), body=TEXT(vector=True, stored=True))

		if not os.path.exists("index"): # create new index if it does not exist yet
			os.mkdir("index")
			self.index = create_in("index", schema)

		self.index = open_dir("index")
		self.writer = self.index.writer()

	def load(self):
		connection = pymongo.Connection("mongodb://viddle_user:viddle_user21@ds037647-a.mongolab.com:37647/db_viddle")
		db = connection.db_viddle

		#for doc in db.links.find({"video":{"$exists":"True"}}):
		#	print(doc)

		for doc in db.links.find({"video":{"$exists":"True"}}):
			texts_len = len(doc["texts"])
			titles_len = len(doc["title"])
			self.add_document(doc["url"], doc["video"], ''.join(doc["title"][0:titles_len]), ''.join(doc["texts"][0:texts_len]))

		self.commit()

	def add_document(self, url, video, title, body):
		print("add_document", url, video, title)
		self.writer.add_document(url=url, video=video, title=title, body=body)

	def commit(self):
		self.writer.commit(optimize=True)

