import sys
import socket
from time import sleep
from chat_lib import create_socket

def client(sock, ip, port):
    while True:
        try:
            print(ip, port, sock)
            sock.connect((ip, port))
            print("connected to", ip, "on port", port)
            return sock
        except ConnectionRefusedError as err:
            # server seems to not be ready for us yet.  We'll retry shortly
            # socket latches into error state, so close it and try again
            sock.close()
            sock = create_socket()
            print("waiting for server")
            sleep(1)
        except OSError as err:
            print("OSError", err)

sock = create_socket()
sock = client(sock, "127.0.0.1", 1234)

while True:
    try:
        text = input(">")
    except EOFError as err:
        print("End of input, closing connection")
        sock.close()
        break

    encoded_text = text.encode('utf-8')

    try:
        bytessent = sock.send(encoded_text)
        print("sent ", bytessent, "bytes")
    except BrokenPipeError as err:
        print("Connection closed by remote end")
        break
