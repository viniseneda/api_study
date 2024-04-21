import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["database"]
mycol = mydb["produtos"]

mydict = { "name": "John", "address": "Highway 37" }

# x = mycol.insert_one(mydict)

# print(x.inserted_id)
for x in mycol.find():
	print(x)

