'''
Defines the HUD objects and communication (TCP) protocol for talking to SimMeR.
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

import pygame
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_q,
    K_e,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import config as CONFIG

class Hud:
    '''Represents the heads up display elements on the canvs.'''

    def __init__(self):
        '''Initialize the robot class'''

        # Indicator color (initial shade of gray)
        self.indicator_color = 240

        # Create the indicator rectangle
        self.ind_pos = CONFIG.border_pixels/4
        self.ind_size = CONFIG.border_pixels/2
        self.indicator = pygame.Rect(self.ind_pos, self.ind_pos, self.ind_size, self.ind_size)

        # Position of pressed key indicators
        self.key_ind_pos = {
            K_w: 1 * (self.ind_size + 2 * self.ind_pos) + self.ind_pos,
            K_a: 2 * (self.ind_size + 2 * self.ind_pos) + self.ind_pos,
            K_s: 3 * (self.ind_size + 2 * self.ind_pos) + self.ind_pos,
            K_d: 4 * (self.ind_size + 2 * self.ind_pos) + self.ind_pos,
            K_q: 5 * (self.ind_size + 2 * self.ind_pos) + self.ind_pos,
            K_e: 6 * (self.ind_size + 2 * self.ind_pos) + self.ind_pos,
        }

        # Color of pressed key indicators
        self.key_ind_colors = {
            K_w: (255, 0, 0),
            K_a: (0, 255, 0),
            K_s: (0, 0, 255),
            K_d: (255, 255, 0),
            K_q: (0, 255, 255),
            K_e: (255, 0, 255),
            'none': (0, 0, 0,)
        }

        # Define pressed key indicator rectangles
        self.key_ind = {
            K_w: pygame.Rect(self.ind_pos, self.key_ind_pos[K_w], self.ind_size, self.ind_size),
            K_a: pygame.Rect(self.ind_pos, self.key_ind_pos[K_a], self.ind_size, self.ind_size),
            K_s: pygame.Rect(self.ind_pos, self.key_ind_pos[K_s], self.ind_size, self.ind_size),
            K_d: pygame.Rect(self.ind_pos, self.key_ind_pos[K_d], self.ind_size, self.ind_size),
            K_q: pygame.Rect(self.ind_pos, self.key_ind_pos[K_q], self.ind_size, self.ind_size),
            K_e: pygame.Rect(self.ind_pos, self.key_ind_pos[K_e], self.ind_size, self.ind_size)
        }

        # Clock for managing game framerate
        self.clock = pygame.time.Clock()

    def check_input(self, events):
        '''Check for keyboard inputs'''

        # Look at every event in the queue
        for event in events:
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    return False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                return False

        return True

    def draw_frame_indicator(self, canvas):
        '''Draws the HUD frame indicator.'''

        # Update the color value
        self.indicator_color -= int(240/CONFIG.frame_rate)
        if self.indicator_color <= 0:
            self.indicator_color = 240

        # Create an RGB color tuple
        color_tuple = (self.indicator_color, self.indicator_color, self.indicator_color)

        # Draw the indicator on the canvas
        pygame.draw.rect(canvas, color_tuple, self.indicator)

    def draw_keys(self, canvas, keypress):
        '''Draws indicators showing the currently pressed wasd-qe keys'''

        for [key, value] in self.key_ind.items():
            if keypress[key]:
                pygame.draw.rect(canvas, self.key_ind_colors[key], self.key_ind[key])
            else:
                pygame.draw.rect(canvas, self.key_ind_colors['none'], self.key_ind[key])

    def get_exec_time(self):
        '''Gets the frame calculation time'''
        return self.clock.get_rawtime()
