from flask import Flask, jsonify, request
from bson.json_util import dumps
from bson.objectid import ObjectId
import bson.errors
import pymongo

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database"]
mycol = mydb["produtos"]
mycol.create_index("nome", unique=True)

def is_number(value):
    return isinstance(value, int) or isinstance(value, float)

def verify_payload_new_product(dict):
    key_list = ('nome', 'preco')

    if len(key_list) != len(dict) or \
    not all(key in dict for key in key_list):
        raise Exception("Estrutura esperada {'nome:\"nome de exemplo\",'preco':\"33,50\"}")
    if (not is_number(dict['preco'])):
        raise Exception("'preco' deve ser um numero")
    if (not isinstance(dict['nome'], str)):
        raise Exception("'nome' deve ser uma string")

def make_message(message):
    return jsonify({"message": message})

@app.route("/", methods=['POST'])
def post_microservice():
    x =  request.json
    try:
        verify_payload_new_product(x)
        mycol.insert_one(x)
    except pymongo.errors.DuplicateKeyError:
        return make_message("Produto ja existe"), 400
    except Exception as e:
        return make_message(str(e)), 400
    return make_message("sucesso"), 200

@app.route("/list", methods=['GET'])
def get_microservice():
    item_list = []
    for item in mycol.find():
        # print(item)
        # print(dumps(item))
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


