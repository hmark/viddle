import sys
import cherrypy
import search
from mako.template import Template
from mako.lookup import TemplateLookup
import os.path
import math

dirname = os.path.dirname(__file__)

CONFIG = dirname + '/conf/dev.conf'
#CONFIG = dirname + '/conf/prod.conf'

tmpl_lookup = TemplateLookup(directories=[dirname + '/templates'], module_directory=dirname + '/tmp/mako_modules', input_encoding='utf-8', output_encoding='utf-8')

class RootPage(object):

	def index(self, term=None):
		tmpl = tmpl_lookup.get_template("index.html")

		query = search.Query()
		
		return tmpl.render_unicode(term=None, data=None, length=-1, newest=query.get_newest(5), help=False)

	def search(self, term=None, page=1):
		tmpl = tmpl_lookup.get_template("index.html")
		
		results_num = 0
		pages = 0
		page = int(page)
		if term != None:
			query = search.Query()
			data, results_num = query.search_term(term, page)
			pages = math.ceil(results_num / 5)

		return tmpl.render_unicode(term=term, data=data, length=results_num, newest=query.get_newest(5), help=False, page=page, pages=pages)

	def help(self):
		tmpl = tmpl_lookup.get_template("index.html")
		return tmpl.render_unicode(term=None, data=None, length=None, newest=None, help=True)

	search.exposed = True
	index.exposed = True
	help.exposed = True

cherrypy.quickstart(RootPage(), '/', CONFIG)
