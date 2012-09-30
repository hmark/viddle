import vidcr.index
import vidcr.dbase
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
				data.append([str(result["url"]), str(result["name"]), "%.2f" % result.score, result["video"][0]])

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
#q.showAll()