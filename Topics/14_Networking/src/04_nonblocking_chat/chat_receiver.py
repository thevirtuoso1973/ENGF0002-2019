import sys
import socket
from time import sleep
from nonblocking_readline import *
from chat_lib import create_socket, server, accept_new_connection

listener_sock = create_socket()
server(listener_sock, 1234)

while True:
    print("listening for incoming connection...")
    sock = accept_new_connection(listener_sock)
    sock.setblocking(False)
    close_conn = False
    while close_conn == False:
        try:
            key_text = nonblocking_readline()
        except (EOFError, KeyboardInterrupt):
            close_conn = True

        if key_text != "":
            encoded_text = key_text.encode('utf-8')
            try:
                bytessent = sock.send(encoded_text)
                print("sent ", bytessent, "bytes")
            except BrokenPipeError as err:
                close_conn = True

        try:
            received_bytes = sock.recv(1024)
            if len(received_bytes) == 0:
                close_conn = True
            else:
                net_text = received_bytes.decode('utf-8')
                print(">>", net_text)
        except BlockingIOError:
            sleep(0.1)

    print("End of input, closing connection")
    sock.close()
