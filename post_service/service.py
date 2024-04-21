from flask import Flask, jsonify, request
import pymongo

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://database:27017/")
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

@app.route("/api/produtos", methods=['POST'])
def post_microservice():
    x =  request.json
    try:
        verify_payload_new_product(x)
        mycol.insert_one(x)
    except pymongo.errors.DuplicateKeyError:
        return make_message("Produto ja existe"), 403
    except Exception as e:
        return make_message(str(e)), 500
    return make_message("Recurso criado"), 201

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0")
