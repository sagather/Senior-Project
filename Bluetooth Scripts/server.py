#This is the script to be run on the raspberry pi

#BEFORE YOU EXECUTE THIS SCRIPT, ON THE R.PI, EXECUTE THE FOLLOWING COMMANDS:
#
#   bluetoothctl        When you run this, it should give you the name of your r.pi
#   pairable on
#   discoverable on
#
#   And then use ctrl+c to escape out, and the pi will be discoverable.  Run the bluetooth tester first, just to verify

import bluetooth

port = 3
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind(("", port))
s.listen(backlog)

client, clientInfo = s.accept()

while 1:
        data = client.recv(size)
        if data:
                print("" + data)

        print("Closing Socket")
        client.close()
        s.close()
