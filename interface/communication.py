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
import time
from threading import Thread
import config.config as CONFIG

class TCPServer:
    '''A TCP Server to listen for command strings from a control algorithm.'''

    def __init__(self):
        '''Instantiation'''

        self.buffer_rx = ''
        self.buffer_tx = ''
        self.loopback = False

        # Socket definition
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((CONFIG.host, CONFIG.port_rx))
        self.sock.listen(5)
        self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock2.bind((CONFIG.host, CONFIG.port_tx))
        self.sock2.listen(5)

        # Threads
        self.listen_thread = Thread(target=self.cmd_listener)
        self.listen_thread.daemon = True
        self.talk_thread = Thread(target=self.response_transmitter)
        self.talk_thread.daemon = True


    def start(self):
        '''Starts running the tcp threads.'''
        self.listen_thread.start()
        self.talk_thread.start()

    def cmd_listener(self):
        '''The main tcp receive loop'''

        # Listen for commands from the command algorithm
        while True:
            # Have the socket accept data
            client_socket, addr = self.sock.accept()
            client_socket.settimeout(CONFIG.timeout)
            with client_socket:
                try:
                    print(f"The robot's socket has been connected to by address: {addr}")

                    # Store the incoming data as a string
                    data = client_socket.recv(1024).decode(CONFIG.str_encoding)

                    # If the receive buffer is empty, act on it. Else dump the data.
                    if not self.buffer_rx:
                        self.buffer_rx = data
                        print(f"The following data was received: {data!r}")
                        # If loopback enabled, respond with a copy of the data
                        if self.loopback:
                            if not self.buffer_tx:
                                self.buffer_tx = data
                            # client_socket.sendall(data.encode(CONFIG.str_encoding))
                    else:
                        print(f"The following data was received: {data!r}, but the receive buffer is full.")
                        if not self.buffer_tx:
                            self.buffer_tx = "Receive Data Buffer is full, please retry in a moment."
                    client_socket.close()

                except TimeoutError:
                    print('Timeout.')

    def response_transmitter(self):
        '''The main tcp transmit loop'''

        while True:
            # Send the response over the socket
            client_socket, addr = self.sock2.accept()
            if self.buffer_tx:
                try:
                    client_socket.send(self.buffer_tx.encode(CONFIG.str_encoding))
                    self.buffer_tx = ''
                except OSError:
                    pass
            time.sleep(1/CONFIG.frame_rate)

    def get_buffer_rx(self):
        '''Get and clear the receive buffer.'''
        if self.buffer_rx:
            data = self.buffer_rx
            self.buffer_rx = ''
            return self.parse_commands(data)
        return []

    def set_buffer_tx(self, data: str):
        '''
        Get and clear the transmit buffer.
        This may end up being unnecessary.
        '''
        if not self.buffer_tx:
            self.buffer_tx = data

    def parse_commands(self, data: str):
        '''
        Parses a command string into a command for the robot to act on.
        [0:1] - The first two characters identify the device to query/command.
        [2] - The third character (optional) should be a hyphen.
        [3:end] - The remaining characters form a data string to tell the device what to do.
        '''

        cmd_id = data[0:2]
        cmd_data = data[3:len(data)]
        cmd = [cmd_id, cmd_data]

        return cmd