'''
Defines the TCP/IP communication functions of the simulator.
'''
# This file is part of SimMeR, an educational mechatronics robotics simulator.
# Initial development funded by the University of Toronto MIE Department.
# Copyright (C) 2023  Ian G. Bennett
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import socket
import time
import math
from threading import Thread
import config as CONFIG

class TCPServer:
    '''A TCP Server to listen for command strings from a control algorithm.'''

    def __init__(self):
        '''Instantiation'''

        self.buffer_rx = ''
        self.buffer_tx = []
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
                    data_raw = client_socket.recv(1024).decode(CONFIG.str_encoding)

                    # Ensure that the received data includes a start and end marker
                    data = self.depacketize(data_raw)

                    if not data:
                        print(f'The following data was recieved but is missing packet framing chars: {data_raw!r}')
                        client_socket.close()
                        continue

                    # If the receive buffer is empty, act on it. Else dump the data.
                    if not self.buffer_rx:
                        self.buffer_rx = data
                        print(f'The following data was received: {data!r}')
                        # If loopback enabled, respond with a copy of the data
                        if self.loopback:
                            if not self.buffer_tx:
                                self.buffer_tx = data
                    else:
                        print(f'The following data was received but the receive buffer is full: {data!r}')
                        if not self.buffer_tx:
                            self.buffer_tx = math.nan
                    client_socket.close()

                except TimeoutError:
                    print('Socket Timeout. Continuing.')
                except ConnectionResetError:
                    print('Socket Connection Reset. Continuing.')

    def response_transmitter(self):
        '''The main tcp transmit loop'''

        while True:
            # Send the response over the socket
            client_socket, _ = self.sock2.accept()
            if self.buffer_tx:
                try:
                    packet = self.make_tx_packet()
                    client_socket.send(packet.encode(CONFIG.str_encoding))
                    self.buffer_tx = []
                except OSError:
                    print("OS Error raised, continuing.")
                except TypeError:
                    print("Invalid tx buffer, flushing.")
                    self.buffer_tx = []
            client_socket.close()
            time.sleep(1/CONFIG.frame_rate)

    def make_tx_packet(self):
        '''
        Build the packet from the responses
        '''
        packet = ''
        for response in self.buffer_tx:
            cmd = response[0]
            value = response[1]
            if isinstance(response[1], float):
                value = round(value, CONFIG.round_digits)
            packet = packet + (f'{cmd}:{value},')
        return self.packetize(packet[:-1])

    def get_buffer_rx(self):
        '''Get and clear the receive buffer.'''
        if self.buffer_rx:
            data = self.buffer_rx
            self.buffer_rx = ''
            return self.parse_commands(data)
        return []

    def parse_commands(self, data: str):
        '''
        Parses a command string into a command for the robot to act on.
        [0:1] - The first two characters identify the device to query/command.
        [2] - The third character (optional) should be a colon.
        [3:end] - The remaining characters form a data string to tell the device what to do.
        '''

        cmds = []
        for cmd in data.split(','):
            cmd_id = cmd[0:2]
            if len(cmd) == 2:
                cmd_data = 0
            else:
                cmd_data = cmd[3:len(cmd)]
            cmds.append([cmd_id, cmd_data])

        return cmds

    def set_buffer_tx(self, responses: list):
        '''
        Put data into the transmit buffer.
        '''
        for response in responses:
            self.buffer_tx.append(response)

    # Packetization and Depacketization functions
    def depacketize(self, data_raw: str):
        '''
        Take a raw string received and verify that it's a complete packet, returning just the data.
        '''


        start = data_raw.find(CONFIG.frame_start)
        end = data_raw.find(CONFIG.frame_end)
        if (start >= 0 and end >= start):
            return data_raw[start+1:end].replace(CONFIG.frame_start + CONFIG.frame_end, ',')
        else:
            return False

    def packetize(self, data: str):
        '''
        Take a message that is to be sent to the command script and packetize it with start and end framing.
        '''

        # Check to make sure that a packet doesn't include any forbidden characters (0x01, 0x02, 0x03, 0x04)
        forbidden = [CONFIG.frame_start, CONFIG.frame_end, '\n']
        check_fail = any(char in data for char in forbidden)

        if not check_fail:
            return CONFIG.frame_start + data + CONFIG.frame_end

        return False
