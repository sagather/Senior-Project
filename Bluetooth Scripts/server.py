#This is the script to be run on the raspberry pi

#BEFORE YOU EXECUTE THIS SCRIPT, ON THE R.PI, EXECUTE THE FOLLOWING COMMANDS:
#
#   bluetoothctl        When you run this, it should give you the name of your r.pi
#   pairable on
#   discoverable on
#
#   And then use ctrl+c to escape out, and the pi will be discoverable.  Run the bluetooth tester first, just to verify

import bluetooth
#import RPi.GPIO as gpio
import time

s = None
client = None

def moveStop():
        gpio.output(17, False)
        gpio.output(27, False)
        gpio.output(19, False)
        gpio.output(26, False)

def moveForward():
        gpio.output(17, False)
        gpio.output(27, True)
        gpio.output(19, False)
        gpio.output(26, True)

def moveReverse():
        gpio.output(17, True)
        gpio.output(27, False)
        gpio.output(19, True)
        gpio.output(26, False)

def moveRotateLeft():
        gpio.output(17, True)
        gpio.output(27, False)
        gpio.output(19, False)
        gpio.output(26, True)

def moveRotateRight():
        gpio.output(17, False)
        gpio.output(27, True)
        gpio.output(19, True)
        gpio.output(26, False)

def setupGPIOPins():
        gpio.setmode(GPIO.BCM)
        gpio.setwarnings(False)
        gpio.setup(17, gpio.out)
        gpio.setup(27, gpio.out)
        gpio.setup(19, gpio.out)
        gpio.setup(26, gpio.out)
        gpio.output(17, False)
        gpio.output(27, False)
        gpio.output(19, False)
        gpio.output(26, False)

def cleanUp():
        if client != None:
                print "Closing Socket"
                client.close()
        if s != None:
                s.close()

        print "Cleaning Up GPIO Pins"
        gpio.cleanup()
        print "Server Closed"

print "Server Started"
exit = 0
while exit != 1:
        setupGPIOPins()
        port = 3
        backlog = 1
        size = 256
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.bind(("", port))
        s.listen(backlog)
        try:
                client, clientInfo = s.accept()
                print "Client Has Connected"
                data = "temp"
                while data:
                        data = client.recv(size)
                        if data:
                                print("Command Received: " + data)
                        if data == "forward":
                                moveForward()
                        elif data == "reverse":
                                moveReverse()
                        elif data == "stop":
                                moveStop()
                        elif data == "left":
                                moveRotateLeft()
                        elif data == "right":
                                moveRotateRight()

        except KeyboardInterrupt:
                print "Closing Server..."
                cleanUp()
                exit = 1

        except:
                print "Error Occured - Restarting Server"
                gpio.cleanup()
