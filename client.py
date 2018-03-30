import bluetooth

#TODO Change the MAC address to your raspberry pi's mac address
#TODO easiest way to find that is to run the bluetooth-tester program on your raspberry pi

serverMACAddress = "B8:27:EB:9E:2A:D6"
port = 3
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))
while 1:
    text = raw_input()
    if text == "quit":
        break
    else:
        s.send(text)
s.close()
