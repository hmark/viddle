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
				
			self.title = parser.title
			self.texts = parser.texts
		else:
			raise Exception("Error: requested URL ", url, " return status code: ", req.status)
