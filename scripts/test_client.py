'''
This file is part of SimMeR, an educational mechatronics robotics simulator.
Initial development funded by the University of Toronto MIE Department.
Copyright (C) 2023  Ian G. Bennett

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

# Basic echo client, for testing purposes
# Code modified from examples on https://realpython.com/python-sockets/

import socket
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT_TX = 61200     # The port used by the *CLIENT* to receive
PORT_RX = 61201     # The port used by the *CLIENT* to send data

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT_TX))
        send_string = input('Type in a string to send: ')
        try:
            s.send(send_string.encode('utf-8'))
        except ConnectionRefusedError:
            print('Tx Connection was refused.')
        except TimeoutError:
            print('Response not received from robot.')

    time.sleep(0.05)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        s2.connect((HOST, PORT_RX))
        try:
            response = s2.recv(1024).decode('utf-8')
            if response:
                print(f'Received {response!r}')
        except TimeoutError:
            print('Response not received from robot.')
        # except ConnectionRefusedError:
        #     print('Rx Connection was refused.')
