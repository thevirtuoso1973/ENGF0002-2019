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

