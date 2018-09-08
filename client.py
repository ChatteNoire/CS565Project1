import socket 

def client():
    """
    Client code for connecting to server and receiving file from server.
    Right now we assume both work on localhost.
    """
    s = socket.socket()   # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 63000   # Make sure that client pings server on correct port

    s.connect((host, port))  # connect with the server
    s.send(b"Hello server!")  # communicate with the server

    # get p, g primes
    p = s.recv(1024)
    g = s.recv(1024)
    with open('received_file', 'wb') as f:
        while True:
            print('Receiving data...')
            data = s.recv(1024)
            print(p)
            print(g)
            print('data=%s', (data))
            if not data:
                break
            # write data to a file
            f.write(data)

    f.close()
    print('Successfully obtained file from server')
    s.close()
    print('Connection closed')

if __name__=='__main__':
    client()
