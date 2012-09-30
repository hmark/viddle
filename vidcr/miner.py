import pymongo
import urllib.request
import parse
import re
import sys
import crawl
import index
import dbase
import log
from datetime import datetime

db = dbase.DBConnection().get_db()
logger = log.Logger()

print("Starting mining...")

# traverse list of sites and crawl data from them
for post in db.sites.find():
	# download html page
	url = post["site"]
	regex = post["regex"]
	response = urllib.request.urlopen(url)
	whoosh = index.Whoosh()

	print("Mining site:", url)

	if response.status == 200: # download is succesfull
		parser = parse.SoupParser()
		parser.parse_html(response)
		anchors = parser.anchors

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

		#print(articles)
		
		# download articles by specified crawler
		if post["crawler"] == "sme.sk":
			crawler = crawl.RegexCrawler()
			crawler.set_regex("meta", "http://i.sme.sk/datamm/.*\.mp4")
		elif post["crawler"] == "youtube":
			crawler = crawl.RegexCrawler()
			crawler.set_regex("iframe","http://www.youtube.com/embed/[0-9A-Za-z_-]{11}")
		elif post["crawler"] == "ted.com":
			crawler = crawl.RegexCrawler()
			crawler.set_regex("a", "http://download.ted.com/talks/.*\.mp4")

		for article in articles:
			#print(db.links.find({"url":article}).count(), article)
			if db.links.find({"url":article}).count() == 0:
				crawler.crawl(article)
				if crawler.video is not None:
					texts_len = len(crawler.texts)
					titles_len = len(crawler.title)
					name_len = len(crawler.name)
					crawler.name = ' '.join(crawler.name[0:name_len])
					crawler.texts = ' '.join(crawler.texts[0:texts_len])
					crawler.title = ' '.join(crawler.title[0:titles_len])

					dt = datetime.now()
					date = dt.strftime("%d.%m.%Y")
					time = dt.strftime("%H:%M")
					db.links.insert({"url":article, "video":crawler.video, "name":crawler.name, "title":crawler.title, "texts":crawler.texts, "date":date, "time":time})
					whoosh.add_document(article, crawler.video, crawler.name, crawler.title, crawler.texts)

					logger.log("new video url: " + article)
				else:
					db.links.insert({"url":article})
					logger.log("new non-video url: " + article)

		whoosh.commit()
	else:
		raise Exception("Error: requested URL ", url, "return status code: ", req.status)


print("Mining succesfully finished.")