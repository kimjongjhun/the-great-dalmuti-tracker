import os
from datetime import datetime
from flask import request, jsonify
from dotenv import load_dotenv
import psycopg2

from app.rounds import rounds_bp
from pgsql import CREATE_ROUNDS_TABLE, GET_ALL_ROUNDS, INSERT_ROUND, DELETE_ROUND, GET_ROUND_BY_ID, UPDATE_ROUND

load_dotenv()
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@rounds_bp.get("/get-all")
def get_all():
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

@rounds_bp.post("/add")
def add():
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

@rounds_bp.delete("/delete/<int:round_id>")
def delete(round_id: int):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(DELETE_ROUND, (round_id,))
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": f"ERROR: {e}"}), 500

    return jsonify({"message": "Round successfully deleted"}), 200

@rounds_bp.patch("/edit/<int:round_id>")
def update(round_id: int):
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
