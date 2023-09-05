'''
Defines the SimMeR block class, which represents the block target for the robot
to pick up.
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

import math
import pygame
import pygame.math as pm
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_q,
    K_e
)
import config as CONFIG
import utilities

class Block():
    '''This class represents the target block'''

    def __init__(self):
        '''Initialize the block class'''

        # Global position information (stored in inches/degrees)
        self.position = pm.Vector2(CONFIG.block_position[0], CONFIG.block_position[1])
        self.rotation = CONFIG.block_rotation

        # Robot size (rectangular)
        self.width = float(CONFIG.block_size)
        self.height = float(CONFIG.block_size)

        # Define the outline of the robot as a polygon
        self.outline = [
            pm.Vector2(-self.width/2, -self.height/2),
            pm.Vector2(-self.width/2,  self.height/2),
            pm.Vector2( self.width/2,  self.height/2),
            pm.Vector2( self.width/2, -self.height/2)
            ]

        self.outline_global = []
        self.outline_global_segments = []
        self.update_outline()

        # Is the robot currently colliding with a maze wall?
        self.collision = False

        # A trail of points where the block has moved
        self.trail = [{
            'position': self.position,
            'rotation': self.rotation,
            'collision': self.collision
        }]

        self.block_square = self._block_square_update()


    def _block_square_update(self):
        '''Updates the line segments that form the block exterior for collision detection.'''
        block_square = [[[self.outline_global[0][0], self.outline_global[0][1]], [self.outline_global[1][0], self.outline_global[1][1]]],
                        [[self.outline_global[1][0], self.outline_global[1][1]], [self.outline_global[2][0], self.outline_global[2][1]]],
                        [[self.outline_global[2][0], self.outline_global[2][1]], [self.outline_global[3][0], self.outline_global[3][1]]],
                        [[self.outline_global[3][0], self.outline_global[3][1]], [self.outline_global[0][0], self.outline_global[0][1]]]]
        return block_square

    def append_trail(self):
        '''Appends current position information to the block's trail'''
        # Not used

        self.trail.append({
            'position': self.position,
            'rotation': self.rotation,
            'collision': self.collision
        })

    def update_outline(self):
        '''
        Define the absolute outline points of the block, in inches, relative
        to the center point of the block.
        '''

        # Rotate the outline
        outline_global = [point.rotate(self.rotation) for point in self.outline]

        # Place the outline in the right location
        self.outline_global = [point + self.position for point in outline_global]

        # Convert the outline points to line segments
        segments = []
        for ct in range(-1, len(self.outline_global) - 1):
            segments.append((self.outline_global[ct], self.outline_global[ct+1]))

        # Update the outline vertices and collision line segments
        self.outline_global_segments = segments
        self.block_square = self._block_square_update()

    def draw(self, canvas):
        '''Draws the block outline on the canvas'''

        # Graphics
        THICKNESS = int(CONFIG.block_thickness * CONFIG.ppi)
        COLOR = CONFIG.block_color

        # Convert the outline from inches to pixels
        outline = [point * CONFIG.ppi + [CONFIG.border_pixels, CONFIG.border_pixels]
                   for point in self.outline_global]

        # Draw the polygon
        pygame.draw.polygon(canvas, COLOR, outline, THICKNESS)

    def move_manual(self, keypress, walls):
        '''Determine the direction to move & rotate the block based on keypresses.'''
        # Not used

        move_vector = pm.Vector2(0, 0)
        rotation = 0
        speed = 6 / CONFIG.frame_rate               # inch/s / frame/s
        rotation_speed = 120 / CONFIG.frame_rate    # deg/s / frame/s

        # Forward/backward movement
        if keypress[K_w]:
            move_vector += [0, speed]
        if keypress[K_s]:
            move_vector += [0, -speed]

        # Left/right movement
        if keypress[K_q]:
            move_vector += [speed, 0]
        if keypress[K_e]:
            move_vector += [-speed, 0]

        # Rotation
        if keypress[K_d]:
            rotation += rotation_speed
        if keypress[K_a]:
            rotation += -rotation_speed

        # Move the robot
        self.move(move_vector, rotation, walls)

    def move(self, velocity, rotation, walls):
        '''Moves the robot, checking for collisions.'''
        # Not used

        # Update robot position
        self.position += pm.Vector2.rotate(velocity, self.rotation)
        self.rotation += rotation
        self.update_outline()

        # Reset the position if a collision is detected
        collisions = self.check_collision_walls(walls)
        if collisions:
            self.position -= pm.Vector2.rotate(velocity, self.rotation)
            self.rotation -= rotation
            self.update_outline()

    def check_collision_walls(self, walls: list):
        '''
        Checks for a collision between the robot's perimeter segments
        and a set of wall line segments.
        '''
        # Not used

        # Loop through all the robot outline line segments, checking for collisions
        for segment_bot in self.outline_global_segments:
            for square in walls:
                for segment_wall in square:
                    collision_points = utilities.collision(segment_bot, segment_wall)
                    if collision_points:
                        return collision_points
