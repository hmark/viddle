from html.parser import HTMLParser

class ViddleHTMLParser(HTMLParser):

	def set_to_default(self):
		self.anchors = []

	def handle_starttag(self, tag, attrs):
		if tag == "a":
			for attr in attrs:
				if attr[0] == "href":
					self.anchors.append(attr[1])
					
# 1. find video content
# 2. if it is not there then exit script
# 3. parse page video data
# 4. parse text data by tags
# 5. return proper number of arrays
