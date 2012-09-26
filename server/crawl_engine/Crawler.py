import pymongo
import urllib.request
import Parser
import re
import sys
import Crawlers

# connect to database
connection = pymongo.Connection("mongodb://viddle_user:viddle_user21@ds037647-a.mongolab.com:37647/db_viddle")
db = connection.db_viddle

# traverse list of sites and crawl data from them
for post in db.sites.find():

	# download html page
	url = post["site"]
	regex = post["regex"]
	response = urllib.request.urlopen(url)

	if response.status == 200: # download is succesfull
		data = response.readlines()
		parser = Parser.ViddleHTMLParser()
		anchors = []

		# find all links in anchor tags
		for line in data:
			line_feed = line.decode("cp1250").encode("utf-8").decode("utf-8")

			if "document.write" in line_feed:
				continue;

			parser.set_to_default()
			parser.feed(line_feed)

			for anchor in parser.anchors:
				anchors.append(anchor)

		links = list(set(anchors))
		
		# filter article links by regex
		articles = []

		# get root domain
		url = "http://" + url.replace("http://", "").split("/")[0]

		for link in links:
			if regex == "NONE" or re.match(re.escape(regex), link):
				# normalize links
				if re.match(r"^http://", link): 
					articles.append(link)
				else:
					articles.append(url + link)

		print(articles)
		
		# download articles by specified crawler
		if post["crawler"] == "sme.sk":
			crawler = Crawlers.SmeCrawler()
		elif post["crawler"] == "youtube":
			crawler = Crawlers.YoutubeCrawler()
		elif post["crawler"] == "ted.com":
			crawler = Crawlers.TedCrawler()


		for article in articles:
			print(article)
			crawler.crawl(article)
			if crawler.video is not None:
				print("VIDEO", crawler.video)

	else:
		raise Exception("Error: requested URL ", url, "return status code: ", req.status)


# 5. parse video link (for embedding in web gui) -> it is index to DocsCollection
# 6. parse documents data (headers, text etc.) -> headers and text are items for this concrete link
# 7. if link already exists in database then EXIT script
# 8. save to DocsCollection data in proper format
# 9. start indexing engine (another class) input->[array of headers, array of navigation, array of words]