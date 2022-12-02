from flask import Flask, jsonify, request
import json
import uuid
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

# Adiciona usuário


@app.route("/user", methods=["POST"])
def create_user():

    response = json.loads(request.data)
    email = response["email"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["email"] == email:
            data = jsonify({
                'statusCode': 302,
                "body": {
                    "message": "Email já cadastrado"
                }
            })
            data.headers.add('Access-Control-Allow-Headers', '*')
            data.headers.add('Access-Control-Allow-Origin', '*')
            data.headers.add("Access-Control-Allow-Methods", '*')

            return data
    file.close()
    users_data.append({
        "id": str(uuid.uuid1()),
        "nome": response["nome"],
        "email": response["email"],
        "senha": response["senha"],
        "categorias": [],
        "reviews": []
    })
    # todo: sobrescrever o conteudo do json
    with open("user_data.json", "w") as newFile:
        json.dump(users_data, newFile)

        data = jsonify(
            {
                'statusCode': 201,
                "body": {
                    "message": "Criado com sucesso"
                }
            }
        )
        data.headers.add('Access-Control-Allow-Headers', '*')
        data.headers.add('Access-Control-Allow-Origin', '*')
        data.headers.add("Access-Control-Allow-Methods", ' *')

        return data


#  Retorna todas as informações do usuario


@app.route("/user", methods=["GET"])
def get_user():

    id = request.args["id"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["id"] == id:
            data = jsonify({
                'statusCode': 200,
                "body": {
                    "message": "Usuário encontrado sucesso",
                    "user": user
                }
            })

            data.headers.add('Access-Control-Allow-Headers', '*')
            data.headers.add('Access-Control-Allow-Origin', '*')
            data.headers.add("Access-Control-Allow-Methods", ' *')
            return data

    data = jsonify({
        'statusCode': 404,
        "body": {
            "message": "Usuário não encontrado"
        }
    })

    data.headers.add('Access-Control-Allow-Headers', '*')
    data.headers.add('Access-Control-Allow-Origin', '*')
    data.headers.add("Access-Control-Allow-Methods", ' *')
    return data

#  Realiza login


@app.route("/login", methods=["POST"])
def login():
    response = json.loads(request.data)
    email = response["email"]
    senha = response["senha"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["email"] == email:
            if user["senha"] == senha:
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Headers': '*',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': '*'
                    },
                    "body": {
                        "message": "Login realizado com sucesso",
                        "data": {
                            "user_id": user["id"],
                            "user_name": user["nome"]
                        }
                    }
                }
            else:
                return {
                    'statusCode': 401,
                    'headers': {
                        'Access-Control-Allow-Headers': '*',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': '*'
                    },
                    "body": {
                        "message": "Senha incorreta"
                    }
                }
    file.close()
    return {
        'statusCode': 404,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        "body": {
            "message": "Usuario não encontrado"
        }
    }


@app.route("/categories", methods=["PUT"])
def editar_categorias():
    response = json.loads(request.data)
    id = response["id"]
    categorias = response["categorias"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["id"] == id:
            user["categorias"] = categorias
            with open("user_data.json", "w") as newFile:
                json.dump(users_data, newFile)
                data = jsonify({
                    'statusCode': 200,
                    "body": {
                        "message": "Categorias adicionadas com sucesso",
                        "categorias": user["categorias"]
                    }
                })
                data.headers.add('Access-Control-Allow-Headers', '*')
                data.headers.add('Access-Control-Allow-Origin', '*')
                data.headers.add("Access-Control-Allow-Methods", ' *')
                return data


@app.route("/review", methods=["POST"])
def create_review():
    response = json.loads(request.data)
    id = response["id"]
    review = response["review"]
    
    print(response)

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["id"] == id:
            user["reviews"].append(
                {
                    "id_review": str(uuid.uuid1()),
                    "title": review["title"],
                    "review": review["review"],
                    "categoria": review["categoria"],
                }
            )
    with open("user_data.json", "w") as newFile:
        json.dump(users_data, newFile)
        data = jsonify({
            'statusCode': 200,
            "body": {
                "message": "Resenha adicionada com sucesso",
                "user": user
            }
        })

        data.headers.add('Access-Control-Allow-Headers', '*')
        data.headers.add('Access-Control-Allow-Origin', '*')
        data.headers.add("Access-Control-Allow-Methods", ' *')
        return data

#


@app.route("/review", methods=["DELETE"])
def delete_review():
    id = request.args["id"]
    id_review = request.args["id_review"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["id"] == id:
            print(user["id"])
            for review in user["reviews"]:
                print(review)
                if review["id_review"] == id_review:
                    user["reviews"].remove(review)
                    with open("user_data.json", "w") as newFile:
                        json.dump(users_data, newFile)
                        data = jsonify({
                            'statusCode': 200,
                            "body": {
                                "message": "Resenha removida com sucesso",
                                "user": user
                            }
                        })
                        data.headers.add('Access-Control-Allow-Headers', '*')
                        data.headers.add('Access-Control-Allow-Origin', '*')
                        data.headers.add("Access-Control-Allow-Methods", ' *')
                        return data

            data = jsonify({
                'statusCode': 404,
                "body": {
                    "message": "Resenha não encontrada"
                }
            })
            data.headers.add('Access-Control-Allow-Headers', '*')
            data.headers.add('Access-Control-Allow-Origin', '*')
            data.headers.add("Access-Control-Allow-Methods", ' *')
            return data