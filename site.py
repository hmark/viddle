import sys
import cherrypy
import search

PRODUCTION = False

class RootPage(object):
	def index(self, term=None):
		return self.header() + self.search_form() + self.footer()

	def search(self, term=None):
		print(term)
		page = self.header() + self.search_form() + "<br>"

		if term != None:
			page += "Searched term: <b>" + term + "</b><br>"
			query = search.Query()
			page += query.search_term(term)

		page += self.footer()

		return page

	def header(self):
		return "<html lang='en'>\
    		<head>\
        		<meta charset='utf-8' /> \
        		<title>Viddle</title>\
        	</head>\
        	<body>"

	def footer(self):
		return "</body>\
			</html>"

	def search_form(self):
		return "<form action='search' method='post' accept-charset='utf-8'>\
			<p>Viddle - video search</p>\
			<input type='text' name='term' value='' size='15' maxlength='30'/>\
			<input type='submit' value='Search'/></p>\
			</form>"

	search.exposed = True
	index.exposed = True

if PRODUCTION:
	print("starting production mode...")
	cherrypy.config.update({
	'engine.autoreload_on': True,
	'environment': 'production',
	'log.screen': False,
	'server.socket_host': '127.0.0.1',
	'server.socket_port': 32108
	})

cherrypy.quickstart(RootPage())
