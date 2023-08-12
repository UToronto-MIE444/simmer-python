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
                        if not self.buffer_rx:
                            self.buffer_rx = data
                            print(f"The following data was received: {data!r}")
                            conn.sendall(data.encode(CONFIG.str_encoding))
                        else:
                            print(f"The following data was received: {data!r}, but the receive buffer is full.")
                            conn.sendall("Receive Data Buffer is full, please retry in a moment.".encode(CONFIG.str_encoding))
                        break

    def get_buffer_rx(self):
        '''Get and clear the receive buffer.'''
        if self.buffer_rx:
            data = self.buffer_rx
            self.buffer_rx = ''
            return self.parse_commands(data)
        return []

    def get_buffer_tx(self):
        '''
        Get and clear the transmit buffer.
        This may end up being unnecessary.
        '''
        data = self.buffer_tx
        self.buffer_tx = ''
        return data

    def parse_commands(self, data: str):
        '''Parses a command string into a list of commands for the robot to act on.'''

        cmd_id = data[0:2]
        cmd_data = data[2:-1]
        cmd = [cmd_id, cmd_data]

        return cmd