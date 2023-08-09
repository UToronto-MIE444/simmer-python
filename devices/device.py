'''
Defines the SimMeR device class.

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
import config.config as CONFIG

class Device():
    '''The base class of all devices that are attached to a robot'''

    def __init__(self, d_id: str, d_type: str, position: list, rotation: float):
        '''Defines the basic information common to all devices'''

        # Device ID string (alphanumeric, lowercase. i.e. "m0")
        self.d_id = d_id

        # Device position and rotation relative to the center point of the robot
        self.position = pygame.math.Vector2(position[0], position[1])
        self.height = 0
        if len(position) > 2:
            self.height = position[2]
        self.rotation = rotation

        # Absolute position, rotation, and outline points
        self.position_a = [0, 0]
        self.rotation_a = 0
        self.pos_update(CONFIG.start_position, CONFIG.start_rotation)
        self.outline_a = []

        # Default display properties
        self.color = (0, 0, 0)
        self.outline_thickness = 0.2
        self.active_color = (255, 0, 0)


    def pos_update(self, bot_pos: pygame.math.Vector2, bot_rot: float):
        '''Updates the absolute position of the device based on its
        relative position and the position of the robot'''
        self.position_a = bot_pos + pygame.math.Vector2.rotate_rad(self.position, bot_rot)
        self.rotation_a = bot_rot + self.rotation


    def define_perimeter(self):
        '''Define the perimeter points of the device, in inches, relative
        to the center point of the robot.'''

        # Rotate the outline
        outline_a = [point.rotate_rad(self.rotation_a) for point in self.outline]

        # Place the outline in the correct
        self.outline_a = [point + self.position_a for point in outline_a]


    def draw(self, canvas: object):
        '''Draws the device on the canvas'''
        THICKNESS = int(self.outline_thickness * CONFIG.ppi)

        outline_a = [point * CONFIG.ppi + [CONFIG.border_pixels, CONFIG.border_pixels]
                   for point in self.outline_a]

        # Draw the polygon
        pygame.draw.polygon(canvas, self.color, outline_a, THICKNESS)
