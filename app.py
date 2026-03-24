
from flask import Flask, jsonify, request
from datetime import datetime
import math
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
            exit_time TIMESTAMP,
            paid_status BOOLEAN DEFAULT 0       
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''
    <h1>Acceso a Parqueadero</h1>

    <form method="post" action="/register">
        <input type="text" name="license_plate" placeholder="Placa" required maxlength="7">
        <select name="action" required>
            <option value="entry">Entrada</option>
            <option value="exit">Salida</option>
        </select>
        <button type="submit">Registrar</button>
    </form>

    <br><br>

    <form method="get" action="/calcular_pago">
        <input type="text" name="license_plate" placeholder="Placa para calcular pago" required>
        <button type="submit">Calcular Pago</button>
    </form>
    '''

def calcular_pago_logica(license_plate):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT entry_time, exit_time 
        FROM parking_records 
        WHERE license_plate = ?
        ORDER BY id DESC LIMIT 1
    ''', (license_plate.upper(),))

    record = cursor.fetchone()
    conn.close()

    if not record:
        return {"error": "No existe registro"}, 404

    entry_time, exit_time = record

    if not exit_time:
        return {"error": "El vehículo aún no ha salido"}, 400

    try:
        ingreso = datetime.strptime(entry_time, "%Y-%m-%d %H:%M:%S")
        salida = datetime.strptime(exit_time, "%Y-%m-%d %H:%M:%S")
    except:
        return {"error": "Formato de fecha inválido"}, 400

    if salida <= ingreso:
        return {"error": "La hora de salida debe ser mayor"}, 400

    diferencia = salida - ingreso
    horas = diferencia.total_seconds() / 3600
    horas_cobradas = math.ceil(horas)

    tarifa_por_hora = 2
    total_pagar = horas_cobradas * tarifa_por_hora

    return {
        "hora_ingreso": entry_time,
        "hora_salida": exit_time,
        "horas_totales": round(horas, 2),
        "horas_cobradas": horas_cobradas,
        "tarifa_por_hora": tarifa_por_hora,
        "total_pagar": total_pagar
    }, 200


@app.route('/api/calcular_pago/<license_plate>', methods=['GET'])
def calcular_pago_api(license_plate):
    data, status = calcular_pago_logica(license_plate)
    return jsonify(data), status

@app.route('/calcular_pago', methods=['GET'])
def calcular_pago_html():
    license_plate = request.args.get('license_plate')
 
    if not license_plate:
        return "<h2>Error: debe ingresar placa</h2><a href='/'>Volver</a>"
 
    data, status = calcular_pago_logica(license_plate)
 
    if status != 200:
        return f"<h2>{data['error']}</h2><a href='/'>Volver</a>"
 
    return f"""
    <h2>Pago para {license_plate.upper()}</h2>
    <p>Hora ingreso: {data['hora_ingreso']}</p>
    <p>Hora salida: {data['hora_salida']}</p>
    <p>Horas totales: {data['horas_totales']}</p>
    <p>Horas cobradas: {data['horas_cobradas']}</p>
    <p>Tarifa por hora: ${data['tarifa_por_hora']}</p>
    <p><strong>Total a pagar: ${data['total_pagar']}</strong></p>
 
    <button onclick="pagar()">Pagar</button>
 
    <script>
    function pagar() {{
        fetch('/api/pagar/{license_plate.upper()}', {{
            method: 'POST'
        }})
        .then(res => res.json())
        .then(data => alert(data.message || data.error))
        .catch(err => alert('Error al procesar pago'));
    }}
    </script>
 
    <br><br>
    <a href="/">Volver</a>
    """



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


@app.route('/api/pagar/<license_plate>', methods=['POST'])
def pagar(license_plate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, exit_time from parking_records where license_plate = ? and paid_status = 0 order by id desc limit 1
    ''', (license_plate.upper(),))
 
    record = cursor.fetchone()
    conn.close()
 
    if not record:
        return jsonify({'error': 'No existe registro pendiente de pago'}), 404
 
    record_id, exit_time = record
 
    if not exit_time:
        return jsonify({'error': 'El vehículo aún no ha salido'}), 400
 
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE parking_records SET paid_status = 1 WHERE id = ?
    ''', (record_id,))
    conn.commit()
    conn.close()
 
    return jsonify({'message': f'Pago procesado para {license_plate.upper()}'}), 200


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=8080)
