import sys
import socket
from chat_lib import create_socket, client

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
