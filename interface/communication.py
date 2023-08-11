'''
Defines the TCP/IP communication functions of the simulator

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

import socket
from threading import Thread
import config.config as CONFIG

class TCPServer:
    '''A TCP Server to listen for command strings from a control algorithm.'''

    def __init__(self):
        '''Instantiation'''

        self.buffer_rx = ''
        self.rx_ready = ''

        self.buffer_tx = ''
        self.tx_ready = ''

        self.listen_thread = Thread(target=self.cmd_listener)
        self.listen_thread.daemon = True

    def start(self):
        '''Starts running the tcp listener thread.'''
        self.listen_thread.start()

    def stop(self):
        '''Not implemented yet. Stops the tcp listener thread from running'''

    def cmd_listener(self):
        '''The main tcp receive loop'''

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as robot_socket:
            robot_socket.bind((CONFIG.host, CONFIG.port))
            robot_socket.listen()
            while True:
                conn, addr = robot_socket.accept()
                with conn:
                    print(f"The robot's socket has been connected to by address: {addr}")
                    while True:
                        data = conn.recv(1024).decode(CONFIG.str_encoding)
                        print(f"The following data was received: {data!r}")
                        print(type(data))
                        conn.sendall(data.encode(CONFIG.str_encoding))
                        break
