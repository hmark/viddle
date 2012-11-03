"""This module contains index search functionality.
"""

import index
import dbase
import re
from whoosh.qparser import MultifieldParser

class Query:
	"""Index search is based on queries. Query finds out indexed data based on term.
	"""

	def search_term(self, term, page):
		"""Term-based index search. Page length is 5.
		Words which are shorter than 3 characters and words with numbers are ignored.
		Search results contains score which is based on inverted index. 
		For more information, check: http://en.wikipedia.org/wiki/Inverted_index
		Results found in titles are boosted by 5.
		Returns results for specified page in descending order.

		:param term: searching term (keywords)
		:param page: results are filtered by this specified page
		"""

		self.whoosh = index.Whoosh()
		parser = MultifieldParser(["title", "body"], schema=self.whoosh.index.schema)
		query = parser.parse(term)
		SCORE_LIMIT = 5

		data = []
		with self.whoosh.index.searcher() as s:
			results = s.search_page(query, page, pagelen=5)

			for result in results:
				tags = s.key_terms([result.docnum], "body", 5)
				taglist = self.create_taglist(tags)

				if result.score > SCORE_LIMIT:
					data.append([str(result["url"]), str(result["name"]), "%.2f" % (result.score - SCORE_LIMIT), result["video"], taglist, result["player"]])

		return data, len(data)

	def create_taglist(self, tags):
		taglist = []
		for tag in tags:
			if len(tag[0]) > 3 and not re.match(r"[0-9]", tag[0]):
				taglist.append(self.translate_word(tag[0]))
		return list(set(taglist))

	def translate_word(self, word):
		"""Used for deriving non-english words with special characters.
		Setup of characters translation: [áäčďéíĺľňóôŕřšťúýžÁČĎÉÍĽŇÓŠŤÚŽ] -> [aacdeillnoorrstuyzacdeilnostuz]
		Returns translated word.
		
		:param word: untranslated word
		"""

		pattern = re.compile(r'[áäčďéíĺľňóôŕšťúýžÁČĎÉÍĽŇÓŠŤÚŽ]')
		trans_table = str.maketrans("áäčďéíĺľňóôŕřšťúýžÁČĎÉÍĽŇÓŠŤÚŽ", "aacdeillnoorrstuyzacdeilnostuz")

		if pattern.findall(word):
			derived_word = word.translate(trans_table)
			return derived_word
		else:
			return word

	def get_newest(self, count):
		"""Last-based mongo database search.
		Returns last added items. Data are obtained from mongo database not index.

		:param count: number of returning items
		"""

		db = dbase.DBConnection().get_db()

		data = []
		for result in db.links.find({ "video": {"$exists": "true"}, "title": {"$exists": "true"}}).sort("_id", -1).limit(count):
			data.append([result["url"], result["name"], result["date"], result["time"], result["video"][0]])

		return data

	#def show_all(self):
	#	self.whoosh = vidcr.index.Whoosh()
	#	reader = self.whoosh.index.reader()
	#	results = reader.all_terms()
	#	for result in results:
	#		print(result)
