# Victoria Van
# CS 565
# September 14, 2018
# Professor T. Mukherjee
# Project 1: Diffie-Hellman *SERVER*
# --------------------------------------
# Description: 
# This program is the server binds to a port and listens to a server
# socket.  The client and server agree on a shared keys 'p' and 'g'
# with the server. Server randomly generates prime 'p2' which is used
# to get Pk2.  The client and server swap public keys and use their own
# private keys to generate the encryption key. The server encrypts the
# input file and sends it the client, which decrypts it with the
# generated key.  The result should be the same as the original input file.
# --------------------------------------
# Code template provided by Professor T.  

'''
File transfer server code. Not multi-threaded.
'''

import socket                   # Import socket module  
import sympy                    # Import symbolic math library - prime generator
import math                     # power function library
from Crypto.Cipher import AES   # AES encryption library
import hashlib                  # hash library (MD5)
import base64                   # binary to plain text library

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
        data = conn.recv(1024)      # Receive from server
        print('Server received', repr(data))

        # Agree on shared prime 'p' and shared key 'g'
        p = sympy.randprime(200,9999)   # random prime generator for 'p'
        print('p = ',p) # print out prime
        g = sympy.randprime(2,1000)     # shared value g
        # Lecture notes!  g = math.exp((1%p)/(p-1))
        print('g = ',g) # print out prime number g
        
        conn.sendall(p.to_bytes(16,'big'))  # send 'p' as bytes, 16 B, big endian
        conn.sendall(g.to_bytes(16,'big'))  # send 'g' to client

        # Generate secret prime 'p2'
        p2 = sympy.randprime(2,2000)    # random prime 'p2'
        while p2 == p:   # p2 != p
            p2 = sympy.randprime(2,2000) # random 'p2' prime (secret)
                
        print('p2 = ',p2) # debugging p2 (only server knows)

        # Generate public key Pk2 = g^(p2) mod p
        Pk2 = pow(g, p2, p) #pow(x,y[,z]) computers g^(y)mod(z) more efficiently
        print ('Pk2 = ',Pk2)

        # Receive Pk1 from Client (1)
        Pk1 = conn.recv(1024)   
        Pk1 = int.from_bytes(Pk1, byteorder='big')  # convert Pk1 bytes -> int
        print('Pk1 = ',Pk1)

        # Send Pk2 to Client (2)
        conn.sendall(Pk2.to_bytes(16,'big'))

        # Get Client Shared Key (3)
        Pk1_p2 = pow(Pk1, p2)
        Pk1_p2 = Pk1_p2 % p     # Pk1_p2 = Pk1^p2 % p
        print('Shared DH key: ', Pk1_p2) # should match with client's Pk2_p1
        
        # file to transfer
        filename='sample.txt'
        f = open(filename,'r') #formerly rb from template (read all at once)
        l = f.read()    # extract contents of file
        l = l.rjust(32) # right justified, width of string
        l = str.encode(l)   # l as a string to bytes
        print('read: ',l)

        # debugging 
        #l = b'Hi there'.rjust(32)
        
        # Encrypt file
        Pk1_p2 = Pk1_p2.to_bytes(16,'big') # convert shared key to bytes
        print(Pk1_p2)
        # AES encryption with key
        cipher = AES.new(Pk1_p2, AES.MODE_ECB) 
        ciphertext = base64.b64encode(cipher.encrypt(l)) # encrypt 'l' file text
        print('Ciphertext: ',ciphertext)
        
        # Implement MD5 hash on Ciphertext
        md5hash = hashlib.md5(ciphertext).hexdigest()
        print(md5hash)
        
        conn.sendall(ciphertext)  #send -> sendall b/c Python3
        print('Sent ',repr(ciphertext)) # print ciphertext sent to client
        f.close()   # close input file
        print('Done sending')
        conn.send(b'File transfer complete!')
        conn.close() # close socket connection

if __name__=='__main__':
    serve()
