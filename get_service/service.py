from flask import Flask, jsonify, request
from bson.json_util import dumps
from bson.objectid import ObjectId
import bson.errors
import pymongo

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://database:27017/")
mydb = myclient["database"]
mycol = mydb["produtos"]

def make_message(message):
    return jsonify({"message": message})

@app.route("/api/produtos", methods=['GET'])
def get_microservice():
    item_list = []
    for item in mycol.find():
        item["_id"] = str(item["_id"])
        item_list.append(item)
    return dumps(item_list), 200

@app.route("/api/produtos/", methods=['GET'])
def get_one_empty():
    return make_message("Id fora do formato"), 400

@app.route("/api/produtos/<product_id>", methods=['GET'])
def get_one(product_id):
    try:
        item = mycol.find_one({"_id": ObjectId(product_id)})
    except bson.errors.InvalidId:
        return make_message("Id fora do formato"), 400
    if not item:
        return "[]", 200
    else:
        item["_id"] = str(item["_id"])
        return dumps(item), 200

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0")
