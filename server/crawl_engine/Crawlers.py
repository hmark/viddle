import urllib.request
import re

class SmeCrawler:

	def crawl(self, url):
		self.url = url

		self.crawlVideo()
		#crawlHeaders()
		#crawlNav()
		#crawlText()

	def crawlVideo(self):
		self.video = None

		response = urllib.request.urlopen(self.url)

		if response.status == 200: # articles download is succesfull
			data = response.readlines()

			for line in data:
				line_feed = line.decode("cp1250").encode("utf-8").decode("utf-8")

				if "document.write" in line_feed:
					continue;

				videos = re.findall("http://i.sme.sk/datamm/.*\.mp4", line_feed)
				if videos:
					self.video = videos[0]
					return
		else:
			raise Exception("Error: requested URL ", url, " return status code: ", req.status)


class YoutubeCrawler:

	def crawl(self, url):
		self.url = url

		self.crawlVideo()
		#crawlHeaders()
		#crawlNav()
		#crawlText()

	def crawlVideo(self):
		self.video = None

		response = urllib.request.urlopen(self.url)

		if response.status == 200: # articles download is succesfull
			data = response.readlines()

			for line in data:
				line_feed = line.decode("cp1250").encode("utf-8").decode("utf-8")

				if "document.write" in line_feed:
					continue;

				videos = re.findall("http://www.youtube.com/embed/[0-9A-Za-z_-]{11}", line_feed)
				if videos:
					self.video = videos[0]
					return
		else:
			raise Exception("Error: requested URL ", url, " return status code: ", req.status)

class TedCrawler:

	def crawl(self, url):
		self.url = url

		self.crawlVideo()
		#crawlHeaders()
		#crawlNav()
		#crawlText()

	def crawlVideo(self):
		self.video = None

		response = urllib.request.urlopen(self.url)

		if response.status == 200: # articles download is succesfull
			data = response.readlines()

			for line in data:
				line_feed = line.decode("cp1250").encode("utf-8").decode("utf-8")

				if "document.write" in line_feed:
					continue;

				videos = re.findall("http://download.ted.com/talks/.*\.mp4", line_feed)
				if videos:
					self.video = videos[0]
					return
		else:
			raise Exception("Error: requested URL ", url, " return status code: ", req.status)
	