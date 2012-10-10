"""This module contains search input and GUI handling.
"""

import sys
import cherrypy
import search
from mako.template import Template
from mako.lookup import TemplateLookup
import os.path
import math

class RootPage(object):
	"""Main page which is powered by CherryPy module.
	Every function specifies get/post call from web browser:
	index - http://viddle.hmark.eu/
	search - http://viddle.hmark.eu/search?term=viddle
	help - http://viddle.hmark.eu/help
	"""

	def index(self):
		"""Index page contains latest videos section.
		"""

		tmpl = tmpl_lookup.get_template("index.html")

		query = search.Query()
		
		return tmpl.render_unicode(term=None, data=None, length=-1, newest=query.get_newest(5), help=False)

	def search(self, term=None, page=1):
		"""Search page contains searched items or "no results" message.
		Number of page is conditioned by total number of searched items and items per page (5).

		:param term: searched term
		:param page: page filter for searched terms
		"""

		tmpl = tmpl_lookup.get_template("index.html")
		
		results_num = 0
		pages = 0
		page = int(page)
		if term != None: # if term is empty then skip search query
			query = search.Query()
			data, results_num = query.search_term(term, page)
			pages = math.ceil(results_num / 5)

		return tmpl.render_unicode(term=term, data=data, length=results_num, newest=query.get_newest(5), help=False, page=page, pages=pages)

	def help(self):
		"""Help page contains basic user manual data.
		"""

		tmpl = tmpl_lookup.get_template("index.html")
		return tmpl.render_unicode(term=None, data=None, length=None, newest=None, help=True)

	search.exposed = True
	index.exposed = True
	help.exposed = True

dirname = os.path.dirname(__file__)

CONFIG = dirname + '/conf/dev.conf'
#CONFIG = dirname + '/conf/prod.conf'

tmpl_lookup = TemplateLookup(directories=[dirname + '/templates'], module_directory=dirname + '/tmp/mako_modules', input_encoding='utf-8', output_encoding='utf-8')


cherrypy.quickstart(RootPage(), '/', CONFIG)
