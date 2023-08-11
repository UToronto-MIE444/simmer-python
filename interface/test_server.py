# Basic echo server, for testing purposes
# Code modified from examples on https://realpython.com/python-sockets/

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    listener.bind((HOST, PORT))
    listener.listen()
    while True:
        conn, addr = listener.accept()
        with conn:
            print(f"The listener has been connected to by address: {addr}")
            while True:
                data = conn.recv(1024).decode('utf-8')
                print(f"The following data was received: {data!r}")
                print(type(data))
                conn.sendall(data.encode('utf-8'))
                break
