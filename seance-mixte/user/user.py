# Importation de datetime pour récupérer la date et l'heure actuelle
import datetime
import json
import uuid

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
    for user in users:
        if user["id"] == user_id:
            user["last_active"] = str(int(datetime.datetime.now().timestamp()))
            save_users()
            break

def save_users():
    """
    Save the users in the database
    :return: None
    """
    with open('{}/data/users.json'.format("."), "w") as users_file:
        json.dump({"users": users}, users_file)


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
        errors.append({"first_name": "first name must not be empty"})

    if "last_name" not in data or data["last_name"].strip() == "":
        errors.append({"last_name": "last name must not be empty"})

    if errors:
        return make_response(jsonify({"errors": errors, "message": "Invalid data"}), 400)

    # id de l'utilisateur
    user_id = str(uuid.uuid4())

    # Verification si l'id est dans la base de donnees
    for user in users:
        if user["id"] == user_id:
            return make_response(jsonify({"error": "User already exists"}), 409)

    user = {
        "id": user_id,
        "name": data["first_name"] + " " + data["last_name"],
        "last_active": str(int(datetime.datetime.now().timestamp()))
    }

    users.append(user)

    save_users()

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

    if "first_name" not in data:
        errors.append({"first_name": "first name must not be empty"})

    if "last_name" not in data:
        errors.append({"last_name": "last name must not be empty"})

    if errors:
        return make_response(jsonify({"errors": errors, "message": "Invalid data"}), 400)

    # Verification si l'id est dans la base de donnees
    for user in users:
        if user["id"] == user_id:
            user["name"] = data["first_name"] + " " + data["last_name"]
            user["last_active"] = str(int(datetime.datetime.now().timestamp()))
            return make_response(jsonify({"message": "User updated", "user": user}), 200)

    save_users()

    return make_response(jsonify({"error": "User not found"}), 404)


@app.route("/user/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    # Verification si l'id est dans la base de donnees
    for user in users:
        if user["id"] == user_id:
            users.remove(user)

            save_users()

            return make_response(jsonify({"message": "User deleted"}), 200)

    return make_response(jsonify({"error": "User not found"}), 404)


##################### Graphql on Movie service #####################
@app.route("/<user_id>/movies", methods=['GET'])
def get_movies(user_id) -> Response:
    """
    Get all the movies
    :return: Response object with all the movies
    """
    update_user_last_active(user_id)

    query = """
    {
      all_movies {
        id
        title
        director
        rating
      }   
    }
    """

    response = requests.post("http://movie:3001/graphql", json={"query": query})

    if response.status_code == 200:
        return make_response(jsonify(response.json()["data"]["all_movies"]), 200)

    return make_response(response.json(), response.status_code)

@app.route("/<user_id>/movies/<movie_id>", methods=['GET'])
def get_movie(user_id, movie_id) -> Response:
    """
    Get a movie by id

    :param user_id: id of the user
    :param movie_id: id of the movie

    :return: Response object with the movie
    """
    update_user_last_active(user_id)

    query = """
    {
      movie_with_id(_id: "%s") {
        id
        title
        director
        rating
        actors {
          id
          firstname
          lastname
        }
      }   
    }
    """ % movie_id

    response = requests.post("http://movie:3001/graphql", json={"query": query})

    if response.status_code == 200:
        response = response.json()["data"]["movie_with_id"]

        if response:
            return make_response(jsonify(response), 200)

        return make_response(jsonify({"error": "Movie not found"}), 404)

    return make_response(response.json(), response.status_code)

@app.route("/<user_id>/movies/<movie_id>/rating/<rating>", methods=['PUT'])
def update_movie_rating(user_id, movie_id, rating) -> Response:
    """
    Update the rating of a movie

    :param user_id: id of the user
    :param movie_id: id of the movie
    :param rating: new rating

    :return: Response object with the movie
    """
    update_user_last_active(user_id)

    mutation = """
    mutation {
      update_movie(_id: "%s", rating: %s) {
        id
        title
        director
        rating
      }
    }
    """ % (movie_id, rating)

    response = requests.post("http://movie:3001/graphql", json={"query": mutation})

    if response.status_code == 200:
        response = response.json()["data"]["update_movie"]

        if response:
            return make_response(jsonify(response), 200)

        return make_response(jsonify({"error": "Movie not found"}), 404)

    return make_response(response.json(), response.status_code)



if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)
