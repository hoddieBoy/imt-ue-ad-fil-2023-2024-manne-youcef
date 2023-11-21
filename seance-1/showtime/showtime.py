from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound
import re

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

@app.route("/showtimes", methods=['GET'])
def get_showtimes():
   return make_response(jsonify(schedule),200)

@app.route("/showtimes/<date>", methods=['GET'])
def get_showtimes_bydate(date):
   # Verification si la date est valide (format YYYYMMDD) avec une regex
   pattern = r'^(\d{4})(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])$'

   if not re.match(pattern, date):
      return make_response(jsonify({"error": "Invalid date format, expected YYYYMMDD"}), 400)
   
   # Verification si la date est dans la base de donnees
   for schedule_date in schedule:
      if schedule_date["date"] == date:
         return make_response(jsonify(schedule_date), 200)
   
   return make_response(jsonify({"error": "Date not found"}), 404)



if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
