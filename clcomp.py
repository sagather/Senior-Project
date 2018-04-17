#   This runs from the laptop

import bluetooth

s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# TODO Change the MAC address to your raspberry pi's mac address
# TODO easiest way to find that is to run the bluetooth-tester program on your raspberry pi


class Client:
    global s

    def __init__(self):

        serverMACAddress = "B8:27:EB:AA:E6:57"  #Cody's car
        #  serverMACAddress = "B8:27:EB:9E:2A:D6"
        port = 3
        #s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.connect((serverMACAddress, port))

    def send(self, text):
            s.send(text)

    def quit(self):
        s.close()
