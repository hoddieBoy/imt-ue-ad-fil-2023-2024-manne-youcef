from flask import Flask, render_template, request, jsonify, make_response
import requests
import json

from werkzeug.exceptions import NotFound
# Importation de datetime pour récupérer la date et l'heure actuelle
import datetime

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/user/", methods=['POST'])
def add_user():
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
   
   # id de l'utilisateur
   user_id = (data["firstname"] + "_" + data["lastname"]).lower()

   # Verification si l'id est dans la base de donnees
   for user in users:
      if user["id"] == user_id:
         return make_response(jsonify({"error": "User already exists"}), 400)

   # La derniere connexion est au moment de l'ajout en secondes
   last_active = str(datetime.datetime.now().timestamp())

   users.append({
      "id": user_id,
      "name": data["firstname"] + " " + data["lastname"],
      "last_active": last_active,
   })
   
   return make_response(jsonify({"message": "User added", "id": user_id}), 201)

@app.route("/user/list", methods=['GET'])
def get_users():
   return make_response(jsonify(users),200)

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

@app.route("/user/<user_id>/bookings", methods=['GET'])
def get_user_bookings(user_id):
   # Vérification si l'id est dans la base de donnees

   check_user = requests.get(f"http://{HOST}:{PORT}/user/{user_id}")

   if check_user.ok:
      return requests.get(f"http://{HOST}:3201/bookings/{user_id}")
   
   return make_response(jsonify({"error": "Impossible to retrieve this user's bookings"}), 404)

@app.route("/user/<user_id>/bookings", methods=['POST'])
def add_user_booking(user_id):
   # Vérification si l'id est dans la base de donnees

   check_user = requests.get(f"http://{HOST}:{PORT}/user/{user_id}")

   if check_user.ok:
      # On interroge le service de réservation

      return requests.post(f"http://{HOST}:3201/bookings/{user_id}", json=request.get_json())
   
   return make_response(jsonify({"error": "Impossible to add this user's bookings"}), 404)

@app.route("/user/<user_id>/movies", methods=['GET'])
def get_user_movies(user_id):
   # Vérification si l'id est dans la base de donnees

   check_user = requests.get(f"http://{HOST}:{PORT}/user/{user_id}")

   if not check_user.ok:
      return make_response(jsonify({"error": "User not found"}), 404)

   # On interroge le service de réservation pour récupérer les réservations de l'utilisateur

   bookings = requests.get(f"http://{HOST}:3201/bookings/{user_id}")

   if not bookings.ok:
      return make_response(jsonify({"error": "Impossible to retrieve this user's bookings"}), 404)

   # On interroge le service de films pour récupérer les films

   movies = requests.get(f"http://{HOST}:3200/movies")

   if not movies.ok:
      return make_response(jsonify({"error": "Impossible to retrieve movies"}), 404)

   # On récupère les films réservés par l'utilisateur

   user_movies = []

   for booking in bookings.json():
      for movie in movies.json():
         if movie["id"] in booking["movies"]:
            user_movies.append(movie)

   return make_response(jsonify(user_movies), 200)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
