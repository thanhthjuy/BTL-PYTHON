from flask import Flask, jsonify, request
import sqlite3
import pandas as pd

app = Flask(__name__)
DATABASE = "players.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/player')
def get_player_by_name():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Thiếu ?name="}), 400

    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM players WHERE player LIKE ?", conn, params=[f"%{name}%"])
    conn.close()

    if df.empty:
        return jsonify({"message": f"Không tìm thấy '{name}'"}), 404
    return jsonify(df.to_dict(orient="records")), 200

@app.route('/api/club')
def get_players_by_club():
    club = request.args.get('club')
    if not club:
        return jsonify({"error": "Thiếu ?club="}), 400

    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM players WHERE club LIKE ?", conn, params=[f"%{club}%"])
    conn.close()

    if df.empty:
        return jsonify({"message": f"Không tìm thấy CLB '{club}'"}), 404
    return jsonify(df.to_dict(orient="records")), 200

if __name__ == '__main__':
    app.run(debug=True)
# http://127.0.0.1:5000/api/player?name=Mohamed Salah
# http://127.0.0.1:5000/api/club?club=Liverpoolư