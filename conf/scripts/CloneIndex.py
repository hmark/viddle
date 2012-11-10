import os
import re
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser
from whoosh.query import Every

#pathname = "../../data/index2"
#schema = Schema(url=ID(stored=True, unique=True), video=ID(stored=True, unique=True), player=TEXT(stored=True), name=TEXT(stored=True), title=TEXT(stored=True, field_boost=5.0), body=TEXT(vector=True, stored=True))
#os.mkdir(pathname)
#newIndex = create_in(pathname, schema)
#newWriter = newIndex.writer()

index = open_dir("../../data/index")
searcher = index.searcher()

parser = MultifieldParser(["title", "body"], schema=index.schema)
query = parser.parse("doprava")
#query = Every()
results_len = 0

with searcher as s:
	results = s.search(query, limit=None)

	for result in results:
		if result.score > 0:
			print(str(result["title"]))
			print(str(result["url"]))
			print("---------------")
			results_len += 1

print("NUMBER OF RESULTS:", results_len)

# delete document by ID
#oldWriter.delete_document(id3)
#oldWriter.delete_document(id2)
#oldWriter.delete_document(id1)
#oldWriter.commit()

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
