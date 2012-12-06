"""This module serves as whoosh index engine mediator.
"""

import os.path
from whoosh.index import open_dir

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

	def close(self):
		"""Close index.
		"""

		self.index.close()
