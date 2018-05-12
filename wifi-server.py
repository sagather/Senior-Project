import socket

_address = "";

s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host, port))

s.listen(5)

while True:
    c, addr = s.accept()
    if addr != _address:
        c.close()
    print("Got connection from ", addr)
    c.send("Connection received")
    c.close()

