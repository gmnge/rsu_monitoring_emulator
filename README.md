# RSU Monitoring Emulator

This project is a Flask application that emulates a RSU monitoring system. The application can be used to simulate the behaviour of a RSU and to visualize the data.

## How does it work?

The data is sent from the lower-level applications, via HTTP POST requests to the proper endpoint (POST /api/vehicle). The RSU Monitoring Emulator stores the incoming data in two different tables, in a SQLite3 database (Filename: 'data.db'). 
1. Table 'device_status': has one single record per Vehicle (the most recent), and might be used in real-time applications.
2. Table 'comm_data': keeps logs of every HTTP request received from the lower level application (most likely a gateway concentrating V2X communication).

The main goal is to create a lightweight, simple and extensible environment to test and debug V2X communication.

## Implemented endpoints/functions
The following functions are defined in the main.py file:

### Web Application endpoints (rendered .html)
1. Homepage (vehicle list)
```python
@app.route('/')
def web_home():
```

2. Vehicle logs page
```python
@app.route('/vehicle/<vehicle_name>', methods=['GET'])
def web_get_vehicle_logs(vehicle_name):
```

3. Reset database page
```python
@app.route('/reset')
def web_reset():
```

### API endpoints (JSON)
1. Generates an array of vehicles (Data format defined in related projects); Front-end application consumes the data
```python
@app.route('/api/vehicle/instant', methods=['GET'])
def api_get_vehicle_list():
```

2. Generates an array of messages related to the chosen vehicle
```python
@app.route('/api/vehicle/<vehicle_name>', methods=['GET'])
def api_get_vehicle_logs(vehicle_name):
```

3. Inserts/updates vehicle information
```python
@app.route('/api/vehicle', methods=['POST'])
def api_update_vehicle():
```

## How run the application
To use the application, first clone the GitHub repository to your local machine. Then, open the main.py file to understand and make eventual changes to meet your requirements.

Don't forget to install the requirements:

```shell
pip install -r requirements.txt
```

Finally, start the Flask internal server by running the following command:

```shell
python3 main.py
```

... or either use the flags --debug to enable debug messages and --reset to reset the database.

The application will be available at http://localhost:5000.

After proper preparation, we recommend deployment using gunicorn to ensure better performance. Just install the requirements on requirements.txt and execute the following command:

```shell
gunicorn -b 0.0.0.0 --workers <number_of_workers> --threads <number_of_threads> main:app
```

I can also generate a README.md file that includes more information, such as the project's dependencies, installation instructions, and usage examples. Just let me know what you need.