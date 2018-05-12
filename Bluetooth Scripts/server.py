#This is the script to be run on the raspberry pi

#BEFORE YOU EXECUTE THIS SCRIPT, ON THE R.PI, EXECUTE THE FOLLOWING COMMANDS:
#
#   bluetoothctl        When you run this, it should give you the name of your r.pi
#   pairable on
#   discoverable on
#
#   And then use ctrl+c to escape out, and the pi will be discoverable.  Run the bluetooth tester first, just to verify

import bluetooth
import RPi.GPIO as gpio
import time

# global vars
s = None
client = None
validMacAddresses = ["18:cf:5e:9d:2c:3f","???"]

def moveStop():
	# Stop the vehicle
	gpio.output(17, False)
        gpio.output(27, False)
        gpio.output(19, False)
        gpio.output(26, False)

def moveForward():
	# Set the vehicle forward
	gpio.output(17, False)
	gpio.output(27, True)
	gpio.output(19, False)
	gpio.output(26, True)

def moveReverse():
	# Reverse the vehicle
	gpio.output(17, True)
	gpio.output(27, False)
	gpio.output(19, True)
	gpio.output(26, False)

def moveRotateLeft():
	# Rotate the vehicle left
	gpio.output(17, True)
	gpio.output(27, False)
        gpio.output(19, False)
	gpio.output(26, True)

def moveRotateRight():
	# Rotate the vehicle right
        gpio.output(17, False)
        gpio.output(27, True)
	gpio.output(19, True)
	gpio.output(26, False)

def setupGPIOPins():
	# Setup the gpio pins
	gpio.setmode(gpio.BCM)
	gpio.setwarnings(False)
	gpio.setup(17, gpio.OUT)
	gpio.setup(27, gpio.OUT)
	gpio.setup(19, gpio.OUT)
	gpio.setup(26, gpio.OUT)
	gpio.setup(23, gpio.OUT) #LED1
	gpio.setup(24, gpio.OUT) #LED2
	gpio.output(17, False)
	gpio.output(27, False)
	gpio.output(19, False)
	gpio.output(26, False)
	gpio.output(23, False)
	gpio.output(24, False)

def cleanUp():
	# Cleanup and close any open resources
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
	gpio.output(23, True)
	port = 3
	backlog = 1
	size = 256
	s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	s.bind(("", port))
	s.listen(backlog)
	try:
		client, clientInfo = s.accept()

		# check if valid trusted connection
		#remoteAddr, resVal = s.getpeername()
		#ret = False
		#for addr in validMacAddresses:
		#	if remoteAddr == addr:
		#		ret = True
		#		break
		#if not ret:
		#	print("Error: Untrusted Client Tried To Connect")
		#	raise RuntimeError("Untrusted Client")

		print "Client Has Connected"
		gpio.output(24, True)
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
		# Close the server
		print "Closing Server..."
		cleanUp()
		exit = 1
	except:
		# An error occured, reinit the server
		print "Error Occured - Restarting Server"
		gpio.cleanup()

