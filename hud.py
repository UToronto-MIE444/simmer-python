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
import pygame
import config as CONFIG

class Hud:
    '''Represents the heads up display elements on the canvs.'''

    def __init__(self):
        '''Initialize the robot class'''
        self.indicator_color = 255

    def draw_frame_indicator(self, canvas):
        '''Draws the HUD frame indicator.'''

        # Create the indicator rectangle
        indicator = pygame.Rect(CONFIG.border_pixels/4, CONFIG.border_pixels/4, CONFIG.border_pixels/2, CONFIG.border_pixels/2)

        # Update the color value
        self.indicator_color -= 1
        if self.indicator_color == -1:
            self.indicator_color = 255

        # Create an RGB color tuple
        color_tuple = (self.indicator_color, self.indicator_color, self.indicator_color)

        # Draw the indicator on the canvas
        pygame.draw.rect(canvas, color_tuple, indicator)