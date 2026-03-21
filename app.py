#API main code for exercise 1
from flask import Flask, jsonify, request
from datetime import datetime
import math

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


