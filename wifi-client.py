import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = "192.168.0.145"      #Stubaru IP at my house
port = 12345                # Reserve a port for your service.

s.connect((host, port))
while 1:
    text = raw_input()
    if text == "quit":
        break
    else:
        s.send(text)
s.close()
s.close                     # Close the socket when done