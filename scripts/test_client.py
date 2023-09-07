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
# and https://www.geeksforgeeks.org/python-display-text-to-pygame-window/

import socket
import struct
from threading import Thread
import _thread
from datetime import datetime
import pygame

def display():

    ### Receive Window Setup ###
    pygame.init()
    clock = pygame.time.Clock()

    # define RGB colors
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    # display size
    X = 400
    Y = 225

    # create the display surface object
    display_surface = pygame.display.set_mode((X, Y))

    # set the pygame window name
    pygame.display.set_caption('Received text')

    # create a font object
    font = pygame.font.Font('freesansbold.ttf', 16)

    # Draw the text field
    display_surface.fill(white)
    pygame.display.update()

    # main loop
    while True:

        responses_rnd = [f"{item:.{2}f}" for item in responses]

        # create a text surface object
        text0 = font.render(f"Last response received at time: {time_rx}", True, green, blue)
        text1 = font.render(f"Last response was: {responses_rnd}", True, green, blue)

        # create a rectangular object for the text surface object
        textRect0 = text0.get_rect()
        textRect1 = text1.get_rect()

        # set the center of the rectangular object
        textRect0.center = (X // 2, Y // 2 + 15)
        textRect1.center = (X // 2, Y // 2 - 15)

        display_surface.fill(white)
        display_surface.blit(text0, textRect0)
        display_surface.blit(text1, textRect1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # deactivate the pygame library and quit the program
                pygame.quit()
                quit()

        # update display
        clock.tick(60)
        pygame.display.flip()

def transmit():
    ask = True
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT_TX))
                if ask:
                    send_string = input('Type in a string to send: ')
                    s.send(send_string.encode('utf-8'))
            except (ConnectionRefusedError, ConnectionResetError):
                print('Tx Connection was refused or reset.')
                _thread.interrupt_main()
            except TimeoutError:
                print('Tx socket timed out.')
                _thread.interrupt_main()
            except EOFError:
                print('\nKeyboardInterrupt triggered. Closing...')
                _thread.interrupt_main()
                ask = False

def receive():
    global responses
    global time_rx
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            try:
                s2.connect((HOST, PORT_RX))
                response_raw = s2.recv(1024)
                if response_raw:
                    responses = bytes_to_list(response_raw)
                    time_rx = datetime.now().strftime("%H:%M:%S")
            except (ConnectionRefusedError, ConnectionResetError):
                print('Rx connection was refused or reset.')
                _thread.interrupt_main()
            except TimeoutError:
                print('Response not received from robot.')
                _thread.interrupt_main()

def bytes_to_list(msg):
    num_responses = int(len(msg)/8)
    data = struct.unpack("%sd" % str(num_responses), msg)
    return data


### Network Setup ###
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT_TX = 61200     # The port used by the *CLIENT* to receive
PORT_RX = 61201     # The port used by the *CLIENT* to send data

# Display text strings
responses = []
time_rx = 'Never'

# Create tx and rx threads
Thread(target = transmit, daemon = True).start()
Thread(target = receive, daemon = True).start()

# Display the received text in a pygame window
try:
    display()
except KeyboardInterrupt:
    pygame.quit()
    quit()
