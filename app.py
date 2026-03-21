#API for register vehicle and get access time to parking lot
from flask import Flask, request, jsonify
from datetime import datetime
app = Flask(__name__)
#In-memory storage for registered vehicles and their access times
registered_vehicles = {}
@app.route('/register', methods=['POST'])
def register_vehicle():
    data = request.get_json()
    license_plate = data.get('license_plate')
    if not license_plate:
        return jsonify({'error': 'License plate is required'}), 400
    access_time = datetime.now().isoformat()
    registered_vehicles[license_plate] = access_time
    return jsonify({'message': f'Vehicle with license plate {license_plate} registered at {access_time}'}), 200
@app.route('/access_time/<license_plate>', methods=['GET'])
def get_access_time(license_plate):
    access_time = registered_vehicles.get(license_plate)
    if not access_time:
        return jsonify({'error': 'Vehicle not found'}), 404
    return jsonify({'license_plate': license_plate, 'access_time': access_time}), 200
if __name__ == '__main__':

