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
import threading
import config.config as CONFIG

class TCPServer:
    '''A TCP Server to listen for command strings from a control algorithm.'''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind((CONFIG.host, CONFIG.port))
        listener.listen()
        while True:
            conn, addr = listener.accept()
            with conn:
                print(f"The listener has been connected to by address: {addr}")
                while True:
                    data = conn.recv(1024).decode(CONFIG.str_encoding)
                    print(f"The following data was received: {data!r}")
                    print(type(data))
                    conn.sendall(data.encode(CONFIG.str_encoding))
                    break