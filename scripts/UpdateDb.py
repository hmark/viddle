import pymongo

db = dbase.DBConnection().get_db()

def reset(self):
	db.links.remove()

def create_field(self):
	db.links.update({"_id":link["_id"]}, {"$set" : {"date" : date, "time" : time}})

def remove_field(self):
	db.links.update({"_id":link["_id"]}, {"$unset" : {"datetime" : 1}}, False, True)