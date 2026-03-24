
from flask import Flask, jsonify, request
from datetime import datetime
import math
import sqlite3
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensaje": "Bienvenido al API del Grupo 7"})

@app.route('/api/calcular_pago', methods=['POST'])
def calcular_pago():
    data = request.get_json()

    hora_ingreso = data.get("hora_ingreso")
    hora_salida = data.get("hora_salida")
    tarifa_por_hora = data.get("tarifa", 1) 

    # Validaciones
    if not hora_ingreso or not hora_salida:
        return jsonify({'error': 'Debe enviar hora_ingreso y hora_salida'}), 400

    try:
        ingreso = datetime.strptime(hora_ingreso, "%Y-%m-%d %H:%M:%S")
        salida = datetime.strptime(hora_salida, "%Y-%m-%d %H:%M:%S")
    except:
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD HH:MM:SS'}), 400

    if salida <= ingreso:
        return jsonify({'error': 'La hora de salida debe ser mayor que la de ingreso'}), 400

    diferencia = salida - ingreso
    
    horas = diferencia.total_seconds() / 3600

    horas_cobradas = math.ceil(horas)

    total_pagar = horas_cobradas * tarifa_por_hora

    return jsonify({
        "hora_ingreso": hora_ingreso,
        "hora_salida": hora_salida,
        "horas_totales": round(horas, 2),
        "horas_cobradas": horas_cobradas,
        "tarifa_por_hora": tarifa_por_hora,
        "total_pagar": total_pagar
    })

if __name__ == '__main__': #Esta linea ejecuta la aplicacion cuando yo en terminal haga python app.py
    app.run(debug=True, host='0.0.0.0', port=8080)


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
@app.route('/records', methods=['GET'])
def get_records():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parking_records')
    records = cursor.fetchall()
    conn.close()
    return jsonify(records)

#clear all records
@app.route('/clear', methods=['GET'])
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