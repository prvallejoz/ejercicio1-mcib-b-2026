from flask import Flask, render_template, request, jsonify
from datetime import datetime
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = "parking.db"

def init_db():
    """Initialize database with parking records table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parking_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_plate TEXT NOT NULL,
            entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            exit_time TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''
    <h1>Acceso a Parqueadero</h1>
    <form method="post" action="/register">
        <input type="text" name="license_plate" placeholder="Placa" required, maxlength="7">
        <select name="action" required>
            <option value="entry">Entrada</option>
            <option value="exit">Salida</option>
        </select>
        <button type="submit">Registrar</button>
    </form>
    '''

@app.route('/register', methods=['POST'])
def register():
    license_plate = request.form.get('license_plate').upper()
    action = request.form.get('action')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if action == 'entry':
        cursor.execute(
            'INSERT INTO parking_records (license_plate) VALUES (?)',
            (license_plate,)
        )
    elif action == 'exit':
        cursor.execute(
            'UPDATE parking_records SET exit_time = CURRENT_TIMESTAMP WHERE license_plate = ? AND exit_time IS NULL',
            (license_plate,)
        )
    
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': f'License plate {license_plate} registered for {action}'})

#Query to get all parking records
@app.route('/registros', methods=['GET'])
def get_records():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parking_records')
    records = cursor.fetchall()
    conn.close()
    return jsonify(records)

#clear all records
@app.route('/clear', methods=['POST'])
def clear_records():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM parking_records')
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'All records cleared'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=8080)