import socket
from chat_lib import create_socket

def client(sock, ip, port):
    # connect the socket to the server
    sock.connect((ip, port))
    print("connected to", ip, "on port", port)
    return sock

sock = create_socket()
sock = client(sock, "127.0.0.1", 1234)

while True:
    text = input(">")
    encoded_text = text.encode()
    sock.send(encoded_text)
