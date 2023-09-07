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
# import time
from threading import Thread
import pygame

def quitter():
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # deactivate the pygame library and quit the program
                pygame.quit()
                quit()

def transmit():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT_TX))
            send_string = input('Type in a string to send: ')
            try:
                s.send(send_string.encode('utf-8'))
            except ConnectionRefusedError:
                print('Tx Connection was refused.')
            except TimeoutError:
                print('Tx socket timed out.')

def receive():

    ### Receive Window Setup ###
    pygame.init()

    # define RGB colors
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    # display size
    X = 400
    Y = 400

    # create the display surface object
    display_surface = pygame.display.set_mode((X, Y))

    # set the pygame window name
    pygame.display.set_caption('Received text')

    # create a font object
    font = pygame.font.Font('freesansbold.ttf', 16)

    # create a text surface object
    text = font.render('RxTextField', True, green, blue)

    # create a rectangular object for the text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object
    textRect.center = (X // 2, Y // 2)

    # Draw the text field
    display_surface.fill(white)
    pygame.display.update()

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            s2.connect((HOST, PORT_RX))
            try:
                response = s2.recv(1024).decode('utf-8')
                if response:
                    print(f'Received {response!r}')
                    display_surface.fill(white)
                    display_surface.blit(text, textRect)
            except TimeoutError:
                print('Response not received from robot.')

### Network Setup ###
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT_TX = 61200     # The port used by the *CLIENT* to receive
PORT_RX = 61201     # The port used by the *CLIENT* to send data

# Create tx and rx threads
Thread(target = transmit).start()
Thread(target = receive).start()

# Check whether pygame has been requested to close
Thread(target = quitter).start()
