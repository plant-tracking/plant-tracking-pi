import bluetooth
import serial


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

socket = connect()

while(True):
    try:
        print socket.recv(1024)
    except bluetooth.btcommon.BluetoothError as error:
        print "Caught BluetoothError: ", error
        time.sleep(5)
        socket = connect()
        pass