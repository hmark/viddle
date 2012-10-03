import sys
import cherrypy
import search
from mako.template import Template
from mako.lookup import TemplateLookup

CONFIG = './conf/dev.conf'
#CONFIG = './conf/prod.conf'

tmpl_lookup = TemplateLookup(directories=['./templates'], module_directory='./tmp/mako_modules', input_encoding='utf-8', output_encoding='utf-8')

class RootPage(object):

	def index(self, term=None):
		tmpl = tmpl_lookup.get_template("index.html")

		query = search.Query()
		
		return tmpl.render_unicode(term=None, data=None, length=-1, newest=query.get_newest(5))

	def search(self, term=None):
		tmpl = tmpl_lookup.get_template("index.html")
		
		length = 0
		if term != None:
			query = search.Query()
			data = query.search_term(term)
			length = len(data)

		return tmpl.render_unicode(term=term, data=data, length=length, newest=query.get_newest(5))

	search.exposed = True
	index.exposed = True

cherrypy.quickstart(RootPage(), '/', CONFIG)
