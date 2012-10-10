"""This module is tracking viddle`s behavior.
"""

from datetime import datetime
import os

class Logger:
	"""Logs text to file which has name specified by actual datetime name.
	"""

	def __init__(self):
		"""Initialize logging file.
		"""

		filename = self.get_actual_datetime()
		print("Logging to file:", filename)
		self.f = open(os.path.dirname(__file__) + "/../data/logs/" + filename + ".log", "w")
		
	def get_actual_datetime(self):
		"""Returns actual datetime.
		"""

		return datetime.now().strftime("%Y-%m-%d.%H-%M")

	def log(self, text):
		"""Log input text to opened file.

		:param text: logging text.
		"""

		self.f.write(text + "\n")
		print(text)
