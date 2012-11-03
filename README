Viddle
======
Web video syndicator.

Changelog
---------
0.5
- extended list of supported sites and video players
- multiple videos per page functionality

0.4
- results pagination
- video templates

0.3
- embedded video output
- tag words

0.2
- slovak text search support
- cherrypy web framework integration

0.1
- web crawling
- data parsering
- basic whoosh indexing and search engine

Dependencies
------------
To run Viddle in your local environment you will need:
1. Python 3.x
2. Whoosh module
3. CherryPy module
4. BeautifulSoup module 
5. PyMongo module
6. MongoDB database

Installation
------------
<code>/data/db.conf</code>
- should contain one line of mongodb access data in format: mongodb://USER:PASS@SITE:PORT/DB_NAME

<code>/data/sites.conf</code>
- list of sites from we are going to crawl inner links with additional sites information
- one line contains triplet [URL INNER_LINKS_FILTER NAME] where:
URL is sites url
INNER_LINKS_FILTER is used for filtering out cross-domain or other irrelevant inner links
NAME is used for identifying site

<code>/data/regex.conf</code>
- list of regular expressions that will be used for finding out video data
- one line contains pair [TAG URL_REGEX] where:
TAG specifies tags from which we are going to crawl video data
URL_REGEX is regular expression for finding out video data
e.g.: input http://embed.ted.com/talks/.*\.html

Usage
-------
Web crawling can be started with miner.py script:
python crawler/miner.py

Search can be executed through web GUI or by query class from search module:
<code>from search import Query
query = search.Query()
query.search_term("internet")</code>
