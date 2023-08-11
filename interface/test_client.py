# Basic echo client, for testing purposes
# Code modified from examples on https://realpython.com/python-sockets/

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

while True:

    send_string = input("Type in a string to send: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(send_string.encode('utf-8'))
        response = s.recv(1024).decode('utf-8')

    print(f"Received {response!r}")
