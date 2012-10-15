"""This module contains data mining script. (it is the heart of Viddle :)
Miner is working in several steps:
1. Initiliaze all modules and download URL of sites from db in which we will look for video data.
2. Traverse list of URLs and crawl anchors from them. (function getAllLinksFromSite())
3. Filter out cross-domain and other irrelevant links. Every URL has own filter. (function filterValidLinksBySiteRegex())
4. Traverse list of filtered inner links and crawl video data from them. (function crawlInnerLinks())
5. Save succesful finds to database and index. (function crawlInnerLinks())
"""

import pymongo
import urllib.request
import parse
import re
import sys
import crawl
import index
import dbase
import log
import logging
from datetime import datetime

def getAllLinksFromSite(response):
	"""Parse anchors from sites response.
	Returns list of anchors (list of hrefs).
	
	:param response: html response
	"""

	parser = parse.SoupParser()
	parser.parse_html(response)
	return list(set(parser.anchors))

def filterValidLinksBySiteRegex(url, regex, links):
	"""Filter valid links (anchor hrefs) by input regular expression.
	Returns matched links.
	
	:param regex: sites regular expression
	:param links: list of anchors (hrefs)
	"""

	url = "http://" + url.replace("http://", "").split("/")[0]
	
	valid_urls = []
	for link in links:
		if re.search(regex, link) and not re.search("\?", link):
			# normalize links to http://... format
			if re.match(r"^http://", link): 
				valid_urls.append(link)
			else:
				valid_urls.append(url + link)

	return valid_urls

def crawlInnerLinks(crawler, whoosh, logger, url):
	"""Crawl data from URL and process output.
	If URL contains video data then save him to mongo database and whoosh index engine.
	If URL does not contain video data then remember this site as a browsed in the mongo database.
	Positive and negative finds are tracking through logger.
	
	:param crawler: sites regular expression
	:param whoosh: list of anchors (hrefs)
	:param logger: list of anchors (hrefs)
	:param url: crawling URL
	"""

	try:
		crawler.crawl(url)
	except urllib.error.HTTPError:
		logger.log("HTTPError: unable to crawl page:", url)

	try:

		if crawler.is_video_found():
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
			whoosh.add_document(url, crawler.video, crawler.player, crawler.name, crawler.title, crawler.texts)

			logger.log("NEW VIDEO:\n")
			logger.log("name: " + crawler.name)
			logger.log("url: " + url)
			logger.log("video: " + crawler.video[0])
			
		else:
			# insert non-video item to database
			#db.links.insert({"url":url})
			logger.log("non-video url: " + url)
	except:
		print(logging.exception(''))

#####################
#### SCRIPT INIT ####
#####################

db = dbase.DBConnection().get_db()
logger = log.Logger()

print("Getting regular expressions...")

crawler = crawl.RegexCrawler()
for entry in db.regexes.find():
	crawler.add_regex(entry["tag"], entry["regex"], entry["player"])

print("Starting mining...")

whoosh = index.Whoosh()
whoosh.clone()

# traverse list of sites and crawl data from them
for post in db.sites.find():
	whoosh.init()

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

whoosh.close()

print("Mining succesfully finished.")