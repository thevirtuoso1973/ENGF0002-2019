import sys
import select
from chat_lib import create_socket, client, server, accept_new_connection

def send_message(sock):
    # read from stdin and send on socket
    key_text = sys.stdin.readline()
    if key_text != "":
        encoded_text = key_text.encode('utf-8')
        bytessent = sock.send(encoded_text)
        print("sent ", bytessent, "bytes")

def recv_message(sock):
    # recv from socket and print to stdout
    received_bytes = sock.recv(1024)
    if len(received_bytes) == 0:
        raise BrokenPipeError()
    else:
        net_text = received_bytes.decode('utf-8')
        print(">>", net_text)

def handle_connection(sock):
    # handle an entire chat connection
    while True:        try:
            # call select to find out if there's any data ready
            rd, wd, ed = select.select([sock, sys.stdin],[],[])

            if sys.stdin in rd:
                send_message(sock)

            if sock in rd:
                recv_message(sock)
                
        except (EOFError, KeyboardInterrupt):
            print("End of input - closing connection")
            break
        except (BrokenPipeError):
            print("Connection closed by peer")
            break

    sock.close()

# act like a server if we use "-s" command line argument
serv = False
for arg in sys.argv:
    if arg == "-s":
        serv = True
        
sock = create_socket()
if serv:
    server(sock, 1234)
    while True:
        try:
            newsock = accept_new_connection(sock)
        except KeyboardInterrupt:
            break
        handle_connection(newsock)
else:
    sock = client(sock, "127.0.0.1", 1234)
    handle_connection(sock)
