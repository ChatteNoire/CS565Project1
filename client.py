import socket
import sympy

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
    print(p)
    print(g)
    p = int.from_bytes(p, byteorder='big')
    g = int.from_bytes(g, byteorder='big')
    print('p = ',p)
    print('g = ',g)
    p1 = sympy.randprime(2,2000)
    print('p1 = ',p1)
    Pk1 = pow(g, p1, p) #pow(x,y[,z]) computers g^(y)mod(z) more efficiently
    print ('Pk1 = ',Pk1)

    # Send Pk1 to Server (1)
    s.sendall(Pk1.to_bytes(10,'big'))

    # Receive Pk2 from Server (2)
    Pk2 = s.recv(1024)
    Pk2 = int.from_bytes(Pk2, byteorder='big')
    print('Pk2 = ',Pk2)
    
    # Get Server Shared Key
    Pk2_p1 = pow(Pk2, p1)
    Pk2_p1 = Pk2_p1 % p
    print('Shared DH key: ', Pk2_p1)
    
    
    with open('received_file', 'wb') as f:
        while True:
            print('Receiving data...')
            data = s.recv(1024)

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
