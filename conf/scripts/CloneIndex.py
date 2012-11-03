import os
import re
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.index import create_in, open_dir

def get_player(video):
	import re

	if re.match(r"^http://i.sme.sk/datamm", video):
		return "sme.sk"
	elif re.match(r"^http://www.youtube.com/embed", video):
		return "youtube.com"
	elif re.match(r"^http://embed.ted.com/talks", video):
		return "ted.com"
	elif re.match(r"^http://video.ted.com", video):
		return "ted.com(old)"

#pathname = "../../data/index2"
#schema = Schema(url=ID(stored=True, unique=True), video=ID(stored=True, unique=True), player=TEXT(stored=True), name=TEXT(stored=True), title=TEXT(stored=True, field_boost=5.0), body=TEXT(vector=True, stored=True))
#os.mkdir(pathname)
#newIndex = create_in(pathname, schema)
#newWriter = newIndex.writer()

oldIndex = open_dir("../../data/index")
oldWriter = oldIndex.writer()
oldSearcher = oldIndex.searcher()

# get document id by URL
id1 = oldSearcher.document_number(url="http://edition.cnn.com/2012/11/03/us/tropical-weather-sandy/index.html")
id3 = oldSearcher.document_number(url="http://edition.cnn.com/2012/11/02/world/europe/turkey-prisons-hunger-strike/index.html")
print(id1, id3)

# delete document by ID
oldWriter.delete_document(id3)
#oldWriter.delete_document(id2)
oldWriter.delete_document(id1)
oldWriter.commit()

#for doc in oldSearcher.reader().all_stored_fields():
	#if re.search(r"\?hpt", doc["url"]):
	#print(doc["url"])
		#print(doc["title"], doc["url"])
	#	id = oldSearcher.document_number(url=doc["url"])
	#	oldWriter.delete_document(id)

#oldWriter.commit()

#for doc in oldSearcher.reader().all_stored_fields():
#	player = get_player(doc["video"][0])
#	newWriter.add_document(url=doc["url"], video=doc["video"], player=player, name=doc["name"], title=doc["title"], body=doc["body"])

#newWriter.commit()
#newSearcher = newIndex.searcher()
#for doc in newSearcher.reader().all_stored_fields():
#	print(doc)
