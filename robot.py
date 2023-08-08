'''
Defines the SimMeR Robot class.

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

class Robot:
    '''This class represents the robot'''

    def __init__(self):
        '''Initialize the robot class'''

        # Position information (stored in inches)
        self.position = CONFIG.start_position
        self.rotation = CONFIG.start_rotation
        self.width = float(CONFIG.robot_width)
        self.height = float(CONFIG.robot_height)

        # Define the outline of the robot as a polygon
        self.outline = [
            pygame.math.Vector2(-self.width/2, -self.height/2),
            pygame.math.Vector2(-self.width/2,  self.height/2),
            pygame.math.Vector2( self.width/2,  self.height/2),
            pygame.math.Vector2( self.width/2, -self.height/2)
            ]

        self.outline_a = []
        self.define_perimeter()

        # Is the robot currently colliding with a maze wall?
        self.collision = False

        # A trail of points where the robot has moved
        self.trail = [{
            "position": self.position,
            "rotation": self.rotation,
            "collision": self.collision
        }]

        # Import the list of devices from the config file
        self.devices = CONFIG.devices

    def append_trail(self):
        '''Appends current position information to the robot's trail'''

        self.trail.append({
            "position": self.position,
            "rotation": self.rotation,
            "collision": self.collision
        })

    def define_perimeter(self):
        '''Define the perimeter points of the robot, in inches, relative
        to the center point of the robot.'''

        # Rotate the outline
        outline_a = [point.rotate_rad(self.rotation) for point in self.outline]

        # Place the outline in the right location
        self.outline_a = [point + self.position for point in outline_a]

    def draw(self, canvas):
        '''Draws the robot outline on the canvas'''

        # Graphics
        THICKNESS = int(CONFIG.robot_thickness * CONFIG.ppi)
        COLOR = CONFIG.robot_color

        outline = [point * CONFIG.ppi + [CONFIG.border_pixels, CONFIG.border_pixels]
                   for point in self.outline_a]

        # Draw the polygon
        pygame.draw.polygon(canvas, COLOR, outline, THICKNESS)


    def check_collision(self):
        '''Check whether there is a collision between the robot and a wall'''

    def parse_commands(self):
        '''Parse text string of commands and act on them'''

    def device_positions(self):
        '''Updates all the absolute positions of all the devices'''

        for device in self.devices.values():
            device.pos_update(self.position, self.rotation)

    def draw_devices(self, canvas):
        '''Draws all devices on the robot onto the canvas'''

        for device in self.devices.values():
            device.draw_device(canvas)
