'''
Defines the SimMeR device super class.
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
import config as CONFIG

class Device():
    '''The base class of all devices that are attached to a robot'''

    def __init__(self, d_id: str, position: list, rotation: float, visible: bool):
        '''Defines the basic information common to all devices'''

        # Device ID string (alphanumeric, lowercase. i.e. "m0")
        self.d_id = d_id

        # Device type (i.e. "drive", "motor", or "sensor")
        self.d_type = ''

        # Device position and rotation relative to the center point of the robot
        self.position = pygame.math.Vector2(position[0], position[1])
        self.height = 0
        if len(position) > 2:
            self.height = position[2]
        self.rotation = rotation
        self.point_vector = pygame.math.Vector2(0, 1).rotate(rotation)

        # Robot perimeter outline placeholder
        self.outline = []

        # Absolute position, rotation, and outline points
        self.position_global = [0, 0]
        self.rotation_global = 0
        self.pos_update(CONFIG.robot_start_position, CONFIG.robot_start_rotation)
        self.outline_global = []

        # Default display properties
        self.color = (0, 0, 0)
        self.outline_thickness = 0.2
        self.active_color = (255, 0, 0)
        self.visible = visible
        self.visible_measurement = False


    def pos_update(self, bot_pos: pygame.math.Vector2, bot_rot: float):
        '''
        Updates the absolute position of the device based on its
        relative position and the position of the robot
        '''
        self.position_global = bot_pos + pygame.math.Vector2.rotate(self.position, bot_rot)
        self.rotation_global = bot_rot + self.rotation


    def update_outline(self):
        '''Define the outline of the device, in inches, in the global reference frame.'''

        # Rotate the outline
        outline_global = [point.rotate(self.rotation_global) for point in self.outline]

        # Place the outline in the correct
        self.outline_global = [point + self.position_global for point in outline_global]


    def draw(self, canvas: object):
        '''Draws the device on the canvas'''
        THICKNESS = int(self.outline_thickness * CONFIG.ppi)

        outline_global = [point * CONFIG.ppi + [CONFIG.border_pixels, CONFIG.border_pixels]
                   for point in self.outline_global]

        # Draw the polygon
        pygame.draw.polygon(canvas, self.color, outline_global, THICKNESS)
