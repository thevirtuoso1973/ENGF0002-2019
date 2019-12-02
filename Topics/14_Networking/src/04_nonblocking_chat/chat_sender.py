import sys
import socket
from time import sleep
from nonblocking_readline import *
from chat_lib import create_socket, client

sock = create_socket()
sock = client(sock, "127.0.0.1", 1234)
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

