import socket
import RPi.GPIO as gpio

#global variables
_s = None
_client = None

#this is the IP the car will eventually be required to connect to once we get the info or once I find out how to make it easy to get that info
_address = ""

def moveStop():
    #stops vehicle
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

    #setup for motor GPIO pins
    gpio.setup(17, gpio.OUT)
    gpio.setup(27, gpio.OUT)
    gpio.setup(19, gpio.OUT)
    gpio.setup(26, gpio.OUT)

    #setup for LED pins
    gpio.setup(23, gpio.OUT)  # LED1
    gpio.setup(24, gpio.OUT)  # LED2

    #initialize everything to OFF
    gpio.output(17, False)
    gpio.output(27, False)
    gpio.output(19, False)
    gpio.output(26, False)
    gpio.output(23, False)
    gpio.output(24, False)

def cleanUp():
    #Cleanup and close open resources
    if _client != None:
        print "Closing Socket"
        _client.close()

    if _s != None:
        _s.close()

    print "Cleaning GPIO pins"
    gpio.cleanup
    print "Server Closed"

#Run the actual server
print "Server Started"
exit = 0
while exit == 0:
    setupGPIOPins()
    gpio.output(23, True)   #Turns on server LED
    port = 12345
    _s = socket.socket()
    host = ""
    _s.bind((host, port))
    _s.listen(5)

    try:
            _client, addr = _s.accept()
            gpio.output(24, True)   #Turns on connection LED

            data = ""

            while data != "exit":
                data = _client.recv(100)
                print "" + data

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
        #Close Server
        print "Closing Server"
        cleanUp()
        exit = 1

    except:
        #Error, server restart
        gpio.cleanup()
