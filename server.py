'''
File transfer server code. Not multi-threaded.
'''

import socket   # Import socket module
from sympy import randprime    # Import symbolic math library - prime generator

port = 63000   # Reserve a port for your service (*client must connect with this port number)
s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
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
        p = randprime(1000,999999)
        
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
