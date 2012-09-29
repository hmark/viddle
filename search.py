import vidcr.index
from whoosh.qparser import MultifieldParser

class Query:

	def search_term(self, term):
		self.whoosh = vidcr.index.Whoosh()
		parser = MultifieldParser(["title", "body"], schema=self.whoosh.index.schema)
		query = parser.parse(term)

		with self.whoosh.index.searcher() as s:
			results = s.search(query)
			roll = str(results.top_n) + "<br>"
			print(results.top_n)
			for result in results:
				#print(result.highlights("title"))
				#roll += str(result)
				#roll += "<br>"
				#print(result)
				roll += "<a href='" + str(result["url"]) + "'>" + str(result["title"]) + "</a><br>"
				#print(result["title"])
				#print(result["body"])

		return roll
