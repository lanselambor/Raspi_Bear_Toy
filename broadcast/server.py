import socket
import time
import threading
import sys
import thread
import os
import time
import subprocess
import tempfile


# sever
aliveFlag = True
clients= []

def broadcast(clients, data):
#    while aliveFlag:    
    print "This is sendThread"
    for i in range(len(clients)):
	clients[i].sendall(data)

def recvThread(conn):
    data = conn.recv(1024).strip()
    if data == '' or data == 'bye':
        aliveFlag = False
        conn.close()
        for i in range(len(clients)):
            if clients[i] == conn:
                del clients[i]
                return      
    while True:
	msg = conn.recv(1024).rstrip()
	if data == "" or data == "bye": 
	    conn.close()
	    return
        else:
            broadcast(clients, data)

# init socket
address = ('localhost', 31500)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
print 'Socket created.'

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
# Bind socket to local host and port
try:
    sock.bind(address)
except socket.error, msg:
    print 'Bind failed.'
    sys.exit()

sock.listen(10) 
print 'Socket listening.'



while True:
    conn, addr = sock.accept()        
    print 'one client connected: ', address

    clients.append(conn)
    
    thread.start_new_thread(recvThread, (conn,))

aliveFlag = False
sock.shutdown()
sock.close()

