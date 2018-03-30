import bluetooth

serverMACAddress = "B8:27:EB:9E:2A:D6"
port = 3
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))
while 1:
    text = raw_input() # Note change to the old (Python 2) raw_input
    if text == "quit":
        break
    else:
        s.send(text)
s.close()


