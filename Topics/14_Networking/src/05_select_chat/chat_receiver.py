import sys
import select
from chat_lib import create_socket, server, accept_new_connection

listener_sock = create_socket()
server(listener_sock, 1234)

while True:
    print("listening for incoming connection...")
    sock = accept_new_connection(listener_sock)
    close_conn = False
    while close_conn == False:
        try:
            # call select to find out if there's any data ready
            rd, wd, ed = select.select([sock, sys.stdin],[],[])
            if sys.stdin in rd:
                key_text = sys.stdin.readline()
                if key_text != "":
                    encoded_text = key_text.encode('utf-8')
                    bytessent = sock.send(encoded_text)
                    print("sent ", bytessent, "bytes")

            if sock in rd:
                received_bytes = sock.recv(1024)
                if len(received_bytes) == 0:
                    close_conn = True
                else:
                    net_text = received_bytes.decode('utf-8')
                    print(">>", net_text)    
        except (EOFError, KeyboardInterrupt, BrokenPipeError):
            close_conn = True

    print("End of input, closing connection")
    sock.close()
