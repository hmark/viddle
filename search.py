import vidcr.index
import vidcr.dbase
import re
from whoosh.qparser import MultifieldParser
#from whoosh.query import Every

class Query:

	def search_term(self, term):
		self.whoosh = vidcr.index.Whoosh()
		parser = MultifieldParser(["title", "body"], schema=self.whoosh.index.schema)
		query = parser.parse(term)

		data = []
		with self.whoosh.index.searcher() as s:
			results = s.search(query)
			results_len = len(results)

			for result in results:
				s_tags = s.key_terms([result.docnum], "body", 5)

				tags = []
				for tag in s_tags:
					if len(tag[0]) > 4 and not re.match(r"[0-9]", tag[0]):
						tags.append(tag[0])
				

				data.append([str(result["url"]), str(result["name"]), "%.2f" % result.score, result["video"][0], tags])

		return data

	def get_newest(self, count):
		db = vidcr.dbase.DBConnection().get_db()

		data = []
		for result in db.links.find({ "video": {"$exists": "true"}, "title": {"$exists": "true"}}).sort("_id", -1).limit(count):
			data.append([result["url"], result["name"], result["date"], result["time"], result["video"][0]])

		return data

	def show_all(self):
		self.whoosh = vidcr.index.Whoosh()
		reader = self.whoosh.index.reader()
		results = reader.all_terms()
		for result in results:
			print(result)

#q = Query()
#print(q.search_term("internet"))