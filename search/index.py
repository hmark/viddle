"""This module serves as whoosh index engine mediator.
"""

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

	def init(self):
		"""Index and writer object initialization.
		If index does not exist then create new in the specified path.
		"""

		pathname = os.path.dirname(__file__) + "/../data/index"
		self.index = open_dir(pathname)
		self.writer = self.index.writer()

	def add_document(self, url, video, player, name, title, body):
		"""Add new document to whoosh writer. Variables must be compatible with index schema.

		:param url: page URL
		:param video: video identificator
		:param player: video player type
		:param name: full name (can contain words with special characters)
		:param title: extended name (can contain derived words)
		:param body: page text
		"""

		self.writer.add_document(url=url, video=video, player=player, name=name, title=title, body=body)

	#def remove_document(self): # USE ONLY IN SPECIAL CASES
	#	self.writer.delete_document(1)

	def commit(self):
		"""Commit all added documents from writer to index.
		"""

		self.writer.commit(optimize=True)

