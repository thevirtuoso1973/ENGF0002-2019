import socket
from time import sleep
from chat_lib import create_socket

def server(sock, port):
    # first we need to bind the socket to a specific port
    sock.bind(('', port))

    # tell the socket to listen for incoming connections
    sock.listen(1)
    print("listening for incoming connection...")

    # Wait here until an incoming connection arrives. When it does,
    # accept it
    client_sock, addr = sock.accept()
    print("Got an incoming connection from ", addr)
    return client_sock

listener_sock = create_socket()
sock = server(listener_sock, 1234)

while True:
    encoded_text = sock.recv(1024)
    text = encoded_text.decode()
    print(text)
