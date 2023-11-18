# Importation de datetime pour récupérer la date et l'heure actuelle
import datetime
import json

import requests
from flask import Flask, request, jsonify, make_response, Response

app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


##################### Utilities #####################
def update_user_last_active(user_id):
    """
    Update the last active date of a user
    :param user_id: id of the user
    :return: None
    """
    index = users.index(user_id)

    if index != -1:
        users[index]["last_active"] = str(datetime.datetime.now().timestamp())


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/user/", methods=['POST'])
def add_user() -> Response:
    """
    Add a user to the database
    :return: Response object with a message and the id of the user
    """
    # Récupération des données de la requête
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Bad request"}), 400)

    # Vérification de la validité des données
    errors = []

    # String vide ou non présent
    if "first_name" not in data or data["first_name"].strip() == "":
        errors.append({"first_name": "Missing field"})

    if "last_name" not in data or data["last_name"].strip() == "":
        errors.append({"last_name": "Missing field"})

    if errors:
        return make_response(jsonify({"errors": errors, "message": "Invalid data"}), 400)

    # id de l'utilisateur
    user_id = (data["first_name"] + "_" + data["last_name"]).lower()

    # Verification si l'id est dans la base de donnees
    for user in users:
        if user["id"] == user_id:
            return make_response(jsonify({"error": "User already exists"}), 400)

    user = {
        "id": user_id,
        "name": data["first_name"] + " " + data["last_name"],
        "last_active": str(datetime.datetime.now().timestamp())
    }

    users.append(user)

    # Mis à jour de la base de données
    with open('{}/data/users.json'.format("."), "w") as jsf:
        json.dump({"users": users}, jsf)

    return make_response(jsonify({"message": "User added", "data": user}), 201)


@app.route("/user/list", methods=['GET'])
def get_users():
    return make_response(jsonify(users), 200)


@app.route("/user/<user_id>", methods=['GET'])
def get_user(user_id):
    # Verification si l'id est dans la base de donnees
    for user in users:
        if user["id"] == user_id:
            return make_response(jsonify(user), 200)

    return make_response(jsonify({"error": "User not found"}), 404)


@app.route("/user/<user_id>", methods=['PUT'])
def update_user(user_id):
    # Récupération des données de la requête
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Bad request"}), 400)

    # Vérification de la validité des données
    errors = []

    if "firstname" not in data:
        errors.append({"firstname": "Missing field"})

    if "lastname" not in data:
        errors.append({"lastname": "Missing field"})

    if errors:
        return make_response(jsonify({"errors": errors}), 400)

    # Verification si l'id est dans la base de donnees
    for user in users:
        if user["id"] == user_id:
            user["name"] = data["firstname"] + " " + data["lastname"]
            return make_response(jsonify({"message": "User updated", "user": user}), 200)

    return make_response(jsonify({"error": "User not found"}), 404)


@app.route("/user/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    # Verification si l'id est dans la base de donnees
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return make_response(jsonify({"message": "User deleted"}), 200)

    return make_response(jsonify({"error": "User not found"}), 404)

if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)
