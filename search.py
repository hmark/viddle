import vidcr.index
from whoosh.qparser import MultifieldParser
#from whoosh.query import Every

class Query:

	def search_term(self, term):
		self.whoosh = vidcr.index.Whoosh()
		parser = MultifieldParser(["title", "body"], schema=self.whoosh.index.schema)
		query = parser.parse(term)

		with self.whoosh.index.searcher() as s:
			results = s.search(query)
			results_len = len(results)

			if results_len == 0:
				roll = "This search did not match any documents."
			else:
				roll = "Results: <b>" + str(results_len) + "</b><br>"
				roll += str(results.top_n) + "<br>"

			print(results.top_n)
			for result in results:
				#print(result.highlights("title"))
				#roll += str(result)
				#roll += "<br>"
				#print(result)
				roll += "<a href='" + str(result["url"]) + "'>" + str(result["name"]) + "</a><br>"
				#print(result["title"])
				#print(result["body"])

		return roll


	def showAll(self):
		self.whoosh = vidcr.index.Whoosh()
		reader = self.whoosh.index.reader()
		results = reader.all_terms()
		for result in results:
			print(result)

#q = Query()
#q.showAll()