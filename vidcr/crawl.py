import urllib.request
import re
import parse

class RegexCrawler:

	def set_regex(self, tag, regex_string):
		self.tag = tag
		self.regex = re.compile(regex_string)

	def crawl(self, url):
		self.url = url
		self.video = None
		self.name = None
		self.title = None
		self.texts = None

		response = urllib.request.urlopen(self.url)

		if response.status == 200: # articles download is succesfull
			parser = parse.SoupParser()
			parser.parse_html(response)

			tags = parser.soup.findAll(self.tag)
			#print(videos)
			for tag in tags:
				parsed_vid = re.findall(self.regex, str(tag))
				#print(parsed_vid)
				if parsed_vid:
					self.video = parsed_vid
					break				
				
			self.name = parser.title
			self.title = list(self.name)
			self.title.extend(self.get_derived_data(self.title)) # special characters duplication
			self.texts = parser.texts
			self.texts.extend(self.get_derived_data(self.texts)) # special characters duplication

			#print(self.name, self.title)
			#print(self.texts)
		else:
			raise Exception("Error: requested URL ", url, " return status code: ", req.status)

	def get_derived_data(self, words):
		derived = []
		pattern = re.compile(r'[áäčďéíĺľňóôŕšťúýž]')
		trans_table = str.maketrans("áäčďéíĺľňóôŕřšťúýž", "aacdeillnoorrstuyz")

		for word in words:
			for s_word in word.split():
				if pattern.findall(s_word):
					derived_word = s_word.translate(trans_table)
					derived.append(derived_word)

		print(derived)
		return derived
