import bluetooth
import serial
import json
import requests


def connect():
    while(True):
        try:
            address = "00:12:03:13:21:49"
            port = 1
            socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            socket.connect((address, port))
            break;
        except bluetooth.btcommon.BluetoothError as error:
            socket.close()
            print "Could not connect: ", error, "; Retrying in 10s..."
            time.sleep(10)
    return socket;

def post_json(body):
    url = "https://planttra.uber.space/nodejs/api/samples"
    headers = {'Content-type': 'application/json'}
    return requests.post(url, data=body, headers=headers)

def handle_value(value):
    objects = plant_value_request_objects(value)
    for object in objects:
	json_data = json.dumps(object)
	print(json_data)
	r = post_json(json_data)
    return

def plant_value_request_objects(plantValue):
    objects = []
    sensorValues = plantValue.split("#")
    for sensorValue in sensorValues:
        object = {}
        if not sensorValue:
            continue
        splittedSensorValue = sensorValue.split("|")
	if len(splittedSensorValue) < 4:
	   continue
	object['plantId'] = 1
	object['type'] = splittedSensorValue[0]
	object['sensorId'] = splittedSensorValue[1]
	object['value'] = splittedSensorValue[2]
	object['unit'] = splittedSensorValue[3]
	objects.append(object)
    return objects

socket = connect()

data = ""
while(True):
    try:
        data += socket.recv(1024)
        data_end = data.find('\n')
        if data_end != -1:
            rec = data[:data_end]
            handle_value(rec)
            data = data[data_end+1:]
    except bluetooth.btcommon.BluetoothError as error:
        print "Caught BluetoothError: ", error
        time.sleep(5)
        socket = connect()
        pass




