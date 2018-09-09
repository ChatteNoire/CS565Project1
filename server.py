'''
File transfer server code. Not multi-threaded.
'''

import socket   # Import socket module
#from sympy import randprime    # Import symbolic math library - prime generator
import sympy
import math

print (b'yooo')

port = 63000   # Reserve a port for your service (*client must connect with this port number)
s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
#s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #reuse addr port immediately stead stuck in TIME_WAIT
s.bind((host, port))  # Bind to the port
s.listen(5)  # Now wait for client connection and listen for requests

def serve():
    """
    The server code. Accepts connections from clients and transfers a file.
    The file should be in the same directory. Ensure that there is only 
    one client connecting. This is not multi-threaded at this point.
    """
    print ('Server listening....')
    while True:
        conn, addr = s.accept()     # Establish connection with client, returns a tuple 
        print ('Got connection from', addr)
        data = conn.recv(1024)
        print('Server received', repr(data))

        #sympy.ntheory.generate.randprime(1000,999999)  # Generate large random prime in range [a,b)
        p = sympy.randprime(200,9999)
        print('p = ',p) #print out prime
        g = sympy.randprime(2,1000)
        # APPARENTLY g isn't random
        # deal with eqn later g = math.exp((1%p)/(p-1))
        print('g = ',g) #print out prime number g
        
        #conn.sendall(p.encode('utf-8'))
        conn.sendall(p.to_bytes(10,'big')) #10 bytes? 
        conn.sendall(g.to_bytes(10,'big'))

        p2 = sympy.randprime(2,2000)
        print('p2 = ',p2)
        Pk2 = pow(g, p2, p) #pow(x,y[,z]) computers g^(y)mod(z) more efficiently
        print ('Pk2 = ',Pk2)

        # Receive Pk1 from Client (1)
        Pk1 = conn.recv(1024)
        Pk1 = int.from_bytes(Pk1, byteorder='big')
        print('Pk1 = ',Pk1)

        # Send Pk2 to Client (2)
        conn.sendall(Pk2.to_bytes(10,'big'))

        # Get Client Shared Key
        Pk1_p2 = pow(Pk1, p2)
        Pk1_p2 = Pk1_p2 % p
        print('Shared DH key: ', Pk1_p2)
        
        # file to transfer
        filename='sample.txt'
        f = open(filename,'rb') #formerly rb
        l = f.read(1024)
        while (l):
            conn.sendall(l) #send -> sendall b/c Python3
            print('Sent ',repr(l))
            l = f.read(1024)
        f.close()
        print('Done sending')
        conn.send(b'File transfer complete!')
        conn.close()

if __name__=='__main__':
    serve()
