import os.path

from whoosh.fields import Schema, TEXT, ID, STORED

path = "../../data/index2"
schema = Schema(url=ID(stored=True, unique=True), video=ID(stored=True, unique=True), name=TEXT(stored=True), title=TEXT(stored=True, field_boost=5.0), body=TEXT(vector=True, stored=True), player=TEXT(stored=True), datetime=TEXT(stored=True))
os.mkdir(path)
