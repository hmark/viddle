"""This module serves as whoosh index engine mediator.
"""

from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.index import create_in, open_dir
import os
import shutil

class Whoosh:
	"""Reads and writes searching data to index engine.
	Check detailed whoosh index specification at http://packages.python.org/Whoosh/
	"""

	def clone(self):
		"""Remove existing target directory and clone there actual index. 
		"""

		path = os.path.dirname(__file__) + "/../data/index"
		target = os.path.dirname(__file__) + "/../data/indexcopy"

		if os.access(target, os.W_OK):
			shutil.rmtree(target)
		shutil.copytree(path, target)

	def init(self):
		"""Index and writer object initialization.
		"""

		target = os.path.dirname(__file__) + "/../data/indexcopy"
		self.index = open_dir(target)
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
		"""Commit all added documents from writer to cloned index.
		"""

		self.writer.commit(optimize=True)

	def close(self):
		"""Release updated index. 
		"""

		self.index.close()

		path = os.path.dirname(__file__) + "/../data/indexcopy"
		target = os.path.dirname(__file__) + "/../data/index"

		shutil.rmtree(target)
		shutil.copytree(path, target)
		shutil.rmtree(path)
