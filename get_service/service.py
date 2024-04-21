from flask import Flask, jsonify, request
from bson.json_util import dumps
from bson.objectid import ObjectId
import bson.errors
import pymongo

myclient = pymongo.MongoClient("mongodb://database:27017/")
mydb = myclient["database"]
mycol = mydb["produtos"]

def make_message(message):
    return jsonify({"message": message})

app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_microservice():
    item_list = []
    for item in mycol.find():
        item["_id"] = str(item["_id"])
        item_list.append(item)
    return dumps(item_list)

@app.route("/<product_id>", methods=['GET'])
def get_one(product_id):
    try:
        item = mycol.find_one({"_id": ObjectId(product_id)})
    except bson.errors.InvalidId:
        return make_message("Id fora do formato"), 400
    if not item:
        return "[]"
    else:
        item["_id"] = str(item["_id"])
        return dumps(item)

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0")
