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
#id1 = oldSearcher.document_number(url="http://www.ted.com/talks/ben_goldacre_what_doctors_don_t_know_about_the_drugs_they_prescribe.html?quote=1877")
#id2 = oldSearcher.document_number(url="http://www.ted.com/talks/robert_gupta_between_music_and_medicine.html?quote=1887")
#id3 = oldSearcher.document_number(url="http://www.ted.com/talks/tim_leberecht_3_ways_to_usefully_lose_control_of_your_reputation.html?quote=1904")
#print(id1, id2, id3)

# delete document by ID
#oldWriter.delete_document(id3)
#oldWriter.delete_document(id2)
#oldWriter.delete_document(id1)
#oldWriter.commit()

for doc in oldSearcher.reader().all_stored_fields():
	#if re.search(r"\?hpt", doc["url"]):
	print(doc["url"])
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
