import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv

from pgsql import CREATE_ROUNDS_TABLE, GET_ALL_ROUNDS, INSERT_ROUND, DELETE_ROUND, GET_ROUND_BY_ID, UPDATE_ROUND

load_dotenv()

app = Flask(__name__)
CORS(app)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.get("/get-all-rounds")
def get_all_rounds():
    rounds = []
    data = {
        "results": [],
        "numberOfPlayers": 0
    }

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(GET_ALL_ROUNDS)
                rounds = cursor.fetchall()
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": f"ERROR: {e}"}), 500
    
    if len(rounds) > 0:
        for round in rounds:
            index, date, results = round

            result = {
                "index": index, "date": date, "playerOrder": results
            }

            data["results"].append(result)

        _,_,players = rounds[0]
        data["numberOfPlayers"] = len(players)

        return jsonify({"message": "Rounds successfully fetched", "data": data}), 200
    else:
        return jsonify({"message": "No rounds to fetch", "data": data}), 200

@app.post("/add-new-round")
def add_new_round():
    data = request.get_json()
    date = datetime.now().date() if not data.get('date') else data['date']
        
    try:
        results = data['results']
    except KeyError as e:
        return jsonify({"error": "Missing info", "message": "Must have round information to save."}), 400

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_ROUNDS_TABLE)
                cursor.execute(INSERT_ROUND, (date, results))
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": f"ERROR: {e}"}), 500

    return jsonify({"message": "Round saved successfully"}), 201

@app.delete("/delete-round/<int:round_id>")
def delete_round(round_id: int):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(DELETE_ROUND, (round_id,))
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": f"ERROR: {e}"}), 500

    return jsonify({"message": "Round successfully deleted"}), 200

@app.patch("/edit-round/<int:round_id>")
def update_round(round_id: int):
    data = request.get_json()
    date = datetime.now().date() if not data.get('date') else data['date']
            
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(GET_ROUND_BY_ID, (round_id,))

                round = cursor.fetchone()
                if round:
                    new_date = round[1] if not data.get('date') else data['date']
                    new_results = round[2] if not data.get('results') else data['results']

                    cursor.execute(UPDATE_ROUND, (new_date, new_results, round_id))
                else:
                    return jsonify({"error": "Request Error", "meesage": "Round to update not found, please check round id"}), 404

        return jsonify({"message": "Round successfully updated", "data": round}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": f"ERROR: {e}"}), 500
    
        