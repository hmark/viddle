import sys
import cherrypy

PORT = 8080
#PORT = 32108

class SearchPage(object):
	def index(self, term=None):
		return "You want to search " + term
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
