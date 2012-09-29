import sys
import cherrypy
import search

PRODUCTION = True

class RootPage(object):
	def index(self, term=None):
		return self.search_form()

	def search(self, term=None):
		page = self.search_form() + "<br>"

		if term != None:
			page += "Searched term: <b>" + term + "</b><br>"
			query = search.Query()
			page += query.search_term(term)

		return page

	def search_form(self):
		return "<form action='search' method='get'>\
			<p>Viddle - video search</p>\
			<input type='text' name='term' value='' size='15' maxlength='30'/>\
			<input type='submit' value='Search'/></p>\
			</form>"

	search.exposed = True
	index.exposed = True

if PRODUCTION:
	print("starting production mode...")
	cherrypy.config.update({
	'environment': 'production',
	'log.screen': False,
	'server.socket_host': '127.0.0.1',
	'server.socket_port': 32108
	})

cherrypy.quickstart(RootPage())
