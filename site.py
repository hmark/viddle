import sys
import cherrypy
import search

PORT = 8080
#PORT = 32108

class SearchPage(object):
	def index(self, term=None):
		page = "Searched term: <b>" + term + "</b><br>"
		query = search.Query()
		page += query.search_term(term)
		#print(page, term)

		return page
	index.exposed = True

	def foo(self):
		return 'Foo!'
	foo.exposed = True

class RootPage(object):
	search = SearchPage()

	def index(self):
		return "<b>Hello World!</b>"
	index.exposed = True

#cherrypy.config.update({
#'environment': 'production',
#'log.screen': False,
#'server.socket_host': '127.0.0.1',
#'server.socket_port': PORT
#})
cherrypy.quickstart(RootPage())
