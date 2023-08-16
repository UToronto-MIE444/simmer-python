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

import math
import pygame
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_q,
    K_e
)
import config.config as CONFIG
import utilities

class Robot():
    '''This class represents the robot'''

    def __init__(self):
        '''Initialize the robot class'''

        # Position information (stored in inches)
        self.position = pygame.math.Vector2(CONFIG.start_position[0], CONFIG.start_position[1])
        self.rotation = CONFIG.start_rotation

        # Robot size (rectangular)
        self.width = float(CONFIG.robot_width)
        self.height = float(CONFIG.robot_height)

        # Define the outline of the robot as a polygon
        self.outline = [
            pygame.math.Vector2(-self.width/2, -self.height/2),
            pygame.math.Vector2(-self.width/2,  self.height/2),
            pygame.math.Vector2( self.width/2,  self.height/2),
            pygame.math.Vector2( self.width/2, -self.height/2)
            ]

        self.outline_global = []
        self.outline_global_segments = []
        self.update_outline()

        # Is the robot currently colliding with a maze wall?
        self.collision = False

        # A trail of points where the robot has moved
        self.trail = [{
            'position': self.position,
            'rotation': self.rotation,
            'collision': self.collision
        }]

        # Import the list of devices from the config file
        self.devices = CONFIG.devices

        # Import the list of drives from the config file
        self.drives = CONFIG.drives

    def append_trail(self):
        '''Appends current position information to the robot's trail'''

        self.trail.append({
            'position': self.position,
            'rotation': self.rotation,
            'collision': self.collision
        })

    def update_outline(self):
        '''
        Define the absolute outline points of the robot, in inches, relative
        to the center point of the robot.
        '''

        # Rotate the outline
        outline_global = [point.rotate_rad(self.rotation) for point in self.outline]

        # Place the outline in the right location
        self.outline_global = [point + self.position for point in outline_global]

        # Convert the outline points to line segments
        segments = []
        for ct in range(-1, len(self.outline_global) - 1):
            segments.append((self.outline_global[ct], self.outline_global[ct+1]))

        self.outline_global_segments = segments

    def draw(self, canvas):
        '''Draws the robot outline on the canvas'''

        # Graphics
        THICKNESS = int(CONFIG.robot_thickness * CONFIG.ppi)
        COLOR = CONFIG.robot_color

        # Convert the outline from inches to pixels
        outline = [point * CONFIG.ppi + [CONFIG.border_pixels, CONFIG.border_pixels]
                   for point in self.outline_global]

        # Draw the polygon
        pygame.draw.polygon(canvas, COLOR, outline, THICKNESS)

    def update_device_positions(self):
        '''
        Updates the global positions and outlines of all the robot's devices.
        '''

        for (d_id, device) in self.devices.items():
            device.pos_update(self.position, self.rotation)
            device.update_outline()

    def draw_devices(self, canvas):
        '''
        Draws all devices on the robot onto the canvas unless marked otherwise.
        '''

        for device in self.devices.values():
            if device.visible:
                device.draw(canvas)
                if device.d_type == 'sensor':
                    device.draw_measurement(canvas)

    def move_manual(self, keypress, walls):
        '''Move the robot manually with the keyboard'''

        velocity = pygame.math.Vector2(0, 0)
        rotation = 0

        # Forward/backward movement
        if keypress[K_w]:
            velocity += [0, 1/CONFIG.ppi]
        if keypress[K_s]:
            velocity += [0, -1/CONFIG.ppi]

        # Left/right movement
        if keypress[K_q]:
            velocity += [1/CONFIG.ppi, 0]
        if keypress[K_e]:
            velocity += [-1/CONFIG.ppi, 0]

        # Rotation
        if keypress[K_d]:
            rotation += math.pi/60
        if keypress[K_a]:
            rotation += -math.pi/60

        # Update robot position
        self.position += pygame.math.Vector2.rotate_rad(velocity, self.rotation)
        self.rotation += rotation
        self.update_outline()

        # Reset the position if a collision is detected
        collisions = self.check_collision_walls(walls)
        if collisions:
            self.position -= pygame.math.Vector2.rotate_rad(velocity, self.rotation)
            self.rotation -= rotation
            self.update_outline()

    def check_collision_walls(self, walls: list):
        '''
        Checks for a collision between the robot's perimeter segments
        and a set of wall line segments.
        '''

        # Loop through all the robot outline line segments, checking for collisions
        for segment_bot in self.outline_global_segments:
            for square in walls:
                for segment_wall in square:
                    collision_points = utilities.collision(segment_bot, segment_wall)
                    if collision_points:
                        return collision_points

    def command(self, cmds: list, environment: dict):
        '''
        Parse text string of commands and act on them, sending them to the appropriate
        device.
        '''

        responses = []
        for cmd in cmds:
            # Get the target device based on ID string, return False if it doesn't exist
            target_device = self.devices.get(cmd[0], False)

            if target_device:
                try:
                    value = float(cmd[1])
                except ValueError:
                    print('Command data (' + cmd[1] + ') not in valid float format. Trying with 0.')
                value = 0
                responses.append(target_device.simulate(value, environment))
            else:
                print('Target device ' + cmd[0] + ' not found.')
                responses.append(math.nan)

        return responses
