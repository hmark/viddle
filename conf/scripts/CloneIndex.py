import os
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

pathname = "../../data/index2"
schema = Schema(url=ID(stored=True, unique=True), video=ID(stored=True, unique=True), player=TEXT(stored=True), name=TEXT(stored=True), title=TEXT(stored=True, field_boost=5.0), body=TEXT(vector=True, stored=True))
os.mkdir(pathname)
newIndex = create_in(pathname, schema)
newWriter = newIndex.writer()

oldIndex = open_dir("../../data/index")
oldWriter = oldIndex.writer()
oldSearcher = oldIndex.searcher()

# get document id by URL
#id1 = oldSearcher.document_number(url="http://tv.sme.sk/v/25315/ucitelia-zavru-skoly-od-26-novembra.html")
#id2 = oldSearcher.document_number(url="http://tv.sme.sk/v/25314/skolski-zamestnanci-budu-strajkovat.html")
#print(id1)
#print(id2)

# delete document by ID
#oldWriter.delete_document(id2)
#oldWriter.delete_document(id1)
#oldWriter.commit()

#for doc in oldSearcher.reader().all_stored_fields():
#	print(doc["player"], doc["url"])

for doc in oldSearcher.reader().all_stored_fields():
	player = get_player(doc["video"][0])
	newWriter.add_document(url=doc["url"], video=doc["video"], player=player, name=doc["name"], title=doc["title"], body=doc["body"])

newWriter.commit()
newSearcher = newIndex.searcher()
for doc in newSearcher.reader().all_stored_fields():
	print(doc)
