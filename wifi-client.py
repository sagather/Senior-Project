import socket               # Import socket module
key = "abcdefghijklmnopqrstuvwxyz"
def encrypt(n, plaintext):
    result = ''

    for l in plaintext.lower():
        try:
            i = (key.index(l) + n) % 26
            result += key[i]
        except ValueError:
            result += l

    return result.lower()

un = "ofpj"
pw = "wtgty"
correct = 0
offset = 5

while correct == 0:
    uninput = raw_input("Enter Your Username: ")
    pwinput = raw_input("Enter Your Password: ")
    if encrypt(5, uninput) == un and encrypt(5, pwinput) == pw:
        correct = 1
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
    else:
        print("Please enter the correct user information")
