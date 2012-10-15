"""This module contains crawler classes related to crawling final data from page.
"""

import urllib.request
import re
import parse

class RegexCrawler:
	"""Regular expression crawler is based on tag-regex pairs. Crawling is realized by function crawl() which 
	start parsing content of page at specified URL. Tag-regex pairs are used one by one to find satisfying video content.
	"""

	def __init__(self):
		"""Initialize regex with related tag arrays.
		Setup is realized by function add_regex().
		"""

		self.tag = []
		self.regexps = []
		self.players = []

	def add_regex(self, tag, regex, player):
		"""Add regex string with related html tag name.

		:param tag: HTML tag where the search will be realized. e.g.: iframe, meta, title...
		:param regex: Regex pattern which describes accepted URLs. e.g.: http://www.youtube.com/embed/[0-9A-Za-z_-]{11}
		:param player: Video player type (based on video site)
		"""

		self.tag.append(tag)
		self.regexps.append(re.compile(regex))
		self.players.append(player)

	def crawl(self, url):
		"""Start crawling data from specified URL. Crawling is realized by list of tags and regular expressions.
		When applied regexps find result in content of specified tags then the content of page is added divided
		to url, video, name, title and texts variable.

		:param url: HTML tag where the search will be realized. e.g.: iframe, meta, title...
		"""

		self.url = url
		self.video = None
		self.name = None
		self.title = None
		self.texts = None

		response = urllib.request.urlopen(self.url)

		if response.status == 200: # page download is succesfull
			parser = parse.SoupParser()
			parser.parse_html(response)

			regex_num = len(self.regexps)
			for i in range(0, regex_num):
				tags = parser.soup.findAll(self.tag[i]) # get all content from tags
				
				for tag in tags:
					parsed_vid = re.findall(self.regexps[i], str(tag)) # find video content based on regex
					
					if parsed_vid:
						self.video = parsed_vid
						self.player = self.players[i]
						break
				else:
					continue
				break

			self.name = parser.title
			self.title = list(self.name)
			self.title.extend(self.get_derived_data(self.title)) # special characters duplication
			self.texts = parser.texts
			self.texts.extend(self.get_derived_data(self.texts)) # special characters duplication
		else:
			raise Exception("Error: requested URL ", url, " return status code: ", req.status)

	def is_video_found(self):
		"""Should be used after crawl function.
		Returns TRUE if the crawler found video with acceptable video name (with at least 1 character).
		"""

		return self.video != None and len(self.name) > 0

	def get_derived_data(self, words):
		"""Used for deriving non-english words with special characters.
		Setup of characters translation: [áäčďéíĺľňóôŕřšťúýžÁČĎÉÍĽŇÓŠŤÚÝŽ] -> [aacdeillnoorrstuyzacdeilnostuyz]
		Returns translated list of words or empty list when there were no translation at all.
		
		:param words: list of words which will be derived to words with non-special characters.
		"""

		derived = []
		pattern = re.compile(r'[áäčďéíĺľňóôŕšťúýž]')
		trans_table = str.maketrans("áäčďéíĺľňóôŕřšťúýžÁČĎÉÍĽŇÓŠŤÚÝŽ", "aacdeillnoorrstuyzacdeilnostuyz")

		for word in words:
			for s_word in word.split():
				if pattern.findall(s_word):
					derived_word = s_word.translate(trans_table)
					derived.append(derived_word)

		return derived
