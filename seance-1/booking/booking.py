from flask import Flask, render_template, request, jsonify, make_response, Response
import requests
import json
import re
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_bookings():
   return make_response(jsonify(bookings),200)

@app.route("/bookings/<user_id>", methods=['GET'])
def get_bookings_byuser(user_id: str) -> Response:
   """
   Get bookings for a specific user
   :param user_id: a specific user id

   :return: Response that contains the bookings for a specific user
   """
   # Verification si l'id est dans la base de donnees
   for booking in bookings:
      if booking["userid"] == user_id:
         return make_response(jsonify(booking), 200)
   
   return make_response(jsonify({"error": "User not found"}), 404)

@app.route("/bookings/<user_id>", methods=['POST'])
def add_booking(user_id: str) -> Response:
   """
    Add a booking for a specific user

   :param str user_id: a specific user id
   :return:
   """
   # Récupération des données de l'utilisateur sinon une liste vide
   user_bookings = bookings.get(user_id, {})
   
   # Récupération des données de la requête
   data = request.get_json()
   if data is None:
      return make_response(jsonify({"error": "Bad request"}), 400)
   
   # Vérification de la validité des données
   errors = []

   if "date" not in data:
      errors.append({"date": "Missing field"})
   elif not re.match(r'^(\d{4})(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])$', data["date"]):
      errors.append({"date": "Invalid date format, expected YYYYMMDD"})
   
   if "movieid" not in data:
      errors.append({"movieid": "Missing field"})
   
   if errors:
      return make_response(jsonify({"errors": errors}), 400)
   
   for booking in user_bookings:
      if booking["date"] == data["date"]:

         if data["movieid"] in booking["movies"]:
            return make_response(jsonify({"error": "Movie already booked for this date"}), 400)
         
         booking["movies"].append(data["movieid"])
         break
   else:
      user_bookings.append({"date": data["date"], "movies": [data["movieid"]]})
   
   bookings[user_id] = user_bookings

   return make_response(jsonify({"message": "Booking added", "user_bookings": user_bookings}), 200)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
