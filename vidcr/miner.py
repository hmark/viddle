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

def getAllLinksFromSite(response):
	parser = parse.SoupParser()
	parser.parse_html(response)
	return list(set(parser.anchors))

def filterValidLinksBySiteRegex(url, regex, links):
	url = "http://" + url.replace("http://", "").split("/")[0]

	valid_urls = []
	for link in links:
		if re.search(regex, link):
			# normalize links to http://... format
			if re.match(r"^http://", link): 
				valid_urls.append(link)
			else:
				valid_urls.append(url + link)

	return valid_urls

def crawlInnerLinks(crawler, whoosh, logger, url):
	try:
		crawler.crawl(url)
	except urllib.error.HTTPError:
		logger.log("HTTPError: unable to crawl page:", url)

	if crawler.video is not None and len(crawler.name) > 0:
		texts_len = len(crawler.texts)
		titles_len = len(crawler.title)
		name_len = len(crawler.name)
		crawler.name = ' '.join(crawler.name[0:name_len])
		crawler.texts = ' '.join(crawler.texts[0:texts_len])
		crawler.title = ' '.join(crawler.title[0:titles_len])

		dt = datetime.now()
		date = dt.strftime("%d.%m.%Y")
		time = dt.strftime("%H:%M")

		# insert new video item to db and index
		db.links.insert({"url":url, "video":crawler.video, "name":crawler.name, "title":crawler.title, "texts":crawler.texts, "date":date, "time":time})
		whoosh.add_document(url, crawler.video, crawler.name, crawler.title, crawler.texts)

		logger.log("NEW VIDEO:")
		logger.log("name: " + crawler.name)
		logger.log("url: " + url)
		logger.log("video: " + crawler.video[0])
		
	else:
		# insert non-video item to database
		db.links.insert({"url":url})
		logger.log("new non-video url: " + url)

#####################
#### SCRIPT INIT ####
#####################

db = dbase.DBConnection().get_db()
logger = log.Logger()

print("Getting regular expressions...")

crawler = crawl.RegexCrawler()
for entry in db.regexes.find():
	crawler.add_regex(entry["tag"], entry["regex"])

print("Starting mining...")

# traverse list of sites and crawl data from them
for post in db.sites.find():
	whoosh = index.Whoosh()

	# download sites html page
	site_url = post["site"]
	site_regex = post["regex"]
	response = urllib.request.urlopen(site_url)

	print("Mining site:", site_url)

	if response.status == 200: # download is succesfull
		links = getAllLinksFromSite(response)
		urls = filterValidLinksBySiteRegex(site_url, site_regex, links)
		
		for url in urls:
			if db.links.find({"url":url}).count() == 0:
				crawlInnerLinks(crawler, whoosh, logger, url)

		whoosh.commit()
	else:
		raise Exception("Error: requested URL ", url, "return status code: ", req.status)


print("Mining succesfully finished.")