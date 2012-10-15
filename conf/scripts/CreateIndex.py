import os.path

path = "../data/index"
schema = Schema(url=ID(stored=True, unique=True), video=ID(stored=True, unique=True), name=TEXT(stored=True), title=TEXT(stored=True, field_boost=5.0), body=TEXT(vector=True, stored=True))
os.mkdir(path)
