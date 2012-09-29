from datetime import datetime
import os

class Logger:

	def __init__(self):
		filename = self.get_actual_datetime()
		print("Logging to file:", filename)
		self.f = open(os.path.dirname(__file__) + "/logs/" + filename + ".log", "w")
		
	def get_actual_datetime(self):
		return datetime.now().strftime("%Y-%m-%d.%I-%M")

	def log(self, text):
		self.f.write(text + "\n")
		print(text)
