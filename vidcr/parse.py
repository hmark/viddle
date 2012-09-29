from bs4 import BeautifulSoup

class SoupParser:

	def parse_html(self, html):
		self.soup = BeautifulSoup(html)

		self.anchors = []
		for link in self.soup.find_all('a'):
			self.anchors.append(link.get('href'))
		
		self.title = ""
		for title in self.soup.find_all('h1'):
			stripped = title.findAll(text=True)
			self.title = stripped

		self.texts = []
		for pTag in self.soup.find_all('p'):
			stripped = pTag.findAll(text=True)
			self.texts.extend(stripped)
			
		#print("h1", self.title)
		#print("p", self.texts)