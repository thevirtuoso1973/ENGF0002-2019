import socket
import sys
from time import sleep

def create_socket():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("socket creation failed with error %s" %(err))
        sys.exit()
    return sock

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

def server(sock, port):
    # first we need to bind the socket to a specific port
    while True:
        try:
            sock.bind(('', port))
            break
        except OSError as err:
            # sometimes the port is still in use; wait til it's free
            print(err)
            print("waiting, will retry in 10 seconds")
            sleep(10)
    # tell the socket to listen for incoming connections
    sock.listen(1)

def accept_new_connection(sock):
    # Wait here until an incoming connection arrives. When it does,
    # accept it
    client_sock, addr = sock.accept()
    print("Got an incoming connection from ", addr)
    return client_sock

