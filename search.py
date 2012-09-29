import index
from whoosh.qparser import MultifieldParser

class Query:

	def search_term(self, term):
		self.whoosh = index.Whoosh()
		parser = MultifieldParser(["title", "body"], schema=self.whoosh.index.schema)
		query = parser.parse(term)

		with self.whoosh.index.searcher() as s:
			results = s.search(query)
			print(results.top_n)
			for result in results:
				#print(result.highlights("title"))
				print(result)
				print(result["title"])
				#print(result["body"])

query = Query()
query.search_term("hlina")