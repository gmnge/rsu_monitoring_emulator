from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap5
import rsu_database as rsu_db
import datetime
import json
import sys
# import helper

# Configs
app = Flask(__name__)
app.secret_key = 'dev'
app.name = 'RSU - Device Monitoring (Emulator)'
bootstrap = Bootstrap5(app)

@app.route('/', methods=['GET'])
def web_home():
    db_device_list = rsu_db.get_vehicle_list() # contains data regarding the connected devices
    return render_template('home.html', device_list=db_device_list, size=len(db_device_list))

@app.route('/reset', methods=['GET'])
def web_reset():
    rsu_db.restart_database()
    db_device_list = rsu_db.get_vehicle_list() # contains data regarding the connected devices
    return render_template('db_reset.html', device_list=db_device_list, size=len(db_device_list))

@app.route('/vehicle/<vehicle_name>', methods=['GET'])
def web_get_vehicle_logs(vehicle_name):
    db_logs = rsu_db.get_vehicle_logs_json_list(vehicle_name)
    # return f"Getting device information for {device_name}"
    return render_template('device.html', logs=db_logs, device_name=vehicle_name)

@app.route('/api/vehicle/instant', methods=['GET'])
def api_get_vehicle_list():
    db_device_list = rsu_db.get_vehicle_list()
    vehicles = {
        'vehicles': []
    }
    for device in db_device_list:
         # fazer testes para fornecer os dados de maneira correta
        device_name = device['sender']
        # device_data_dict = eval(device['data']).replace("'", '"') 
        device_data_json = json.loads(device['data'])
        # print(type(device_data_json))
        
        velocity = device_data_json['velocity']
        angle = device_data_json['angle']
        distance = device_data_json['distance']
        vehicles['vehicles'].append(
            {
                'overview': {
                    'name': device_name,
                    'isLeader': False,
                    'velocity': {
                        'icon': 'speed',
                        'value': str(velocity)
                    },
                    'angle': {
                        'icon':'speed',
                        'value': str(angle)
                    },
                    'distance': {
                        'icon':'speed',
                        'value': str(distance)
                    }
                }
            }
        )
        pass
    return jsonify(vehicles)

@app.route('/api/vehicle/<vehicle_name>', methods=['GET'])
def api_get_vehicle_logs(vehicle_name):
    db_logs = rsu_db.get_vehicle_logs_json_list(vehicle_name)
    list_of_logs = []

    # Garantir conversão do elemento data em um dicionário na lista retornada na API
    for log in db_logs:
        log['data'] = json.loads(log['data'])
        # print(log['data'])
        # print(type(log['data']))
        list_of_logs.append(log)
    
    return list_of_logs

@app.route('/api/vehicle', methods=['POST'])
def api_update_vehicle():
    # CURL EXAMPLE
    # curl -X POST http://localhost:5000/device -H 'Content-Type: application/json' -d '{"sender":"vehicle1",receiver: "vehicle2", "data":"data_127361827361827"}'
    errors = []
    if request.method == "POST":
        # get url that the user has entered
        try:
            # gets the payload of the request in plain-text below
            # content = request.get_data().decode()
            # gets a json from the request's payload    
            request_payload_json = request.json

            sender = "ND"
            receiver = "ND"
            data = {}
            # save json values into variables
            try:
                sender = request_payload_json['sender']
            except:
                pass
            try:
                receiver = request_payload_json['receiver']
            except:
                pass
            try:
                data = str(request_payload_json['data'])
            except:
                pass
            
            # debug printing below
            # print(request.remote_addr+" - Devices: "+sender+" / "+receiver+" - Data: "+data)
            # columns = ['sender', 'receiver', 'data', 'timestamp']
            values = [sender, receiver, json.dumps(data), datetime.datetime.now()]  # Replace with the values for the new line
            rsu_db.update_vehicle(values)
            return '', 200
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return '', 404


if __name__ == '__main__':
    try:
        if sys.argv.index('--reset') != -1:
            rsu_db.restart_database()
        if sys.argv.index('--debug') == -1:
            app.run(debug=False, host='0.0.0.0')
        else:
            app.run(debug=True, host='0.0.0.0')
    except:
        app.run(debug=False, host='0.0.0.0')
        
    

