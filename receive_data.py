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

def handle_value(value):
    payload = plant_value_as_json(value)
    url = "asdf"
    # r = requests.post(url, data=payload)
    print(r.text)
    return

def plant_value_as_json(plantValue):
    object = {}
    sensorValues = plantValue.split("#")
    for sensorValue in sensorValues:
        if not sensorValue:
            continue
        splittedSensorValue = sensorValue.split("|")
        object[splittedSensorValue[0]] = splittedSensorValue[len(splittedSensorValue)-1]
    return json.dumps(object)

socket = connect()

data = ""
while(True):
    try:
        data += socket.recv(1024)
        data_end = data.find('\n')
        if data_end != -1:
            rec = data[:data_end]
            handle_value(data)
            data = data[data_end+1:]
    except bluetooth.btcommon.BluetoothError as error:
        print "Caught BluetoothError: ", error
        time.sleep(5)
        socket = connect()
        pass




