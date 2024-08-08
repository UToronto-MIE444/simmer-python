'''
Defines the SimMeR Robot class.
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
    K_e,
    K_t
)
import config as CONFIG
import utilities

class Robot():
    '''This class represents the robot'''

    def __init__(self):
        '''Initialize the robot class'''

        # Position information (stored in inches)
        self.position = pm.Vector2(CONFIG.robot_start_position[0], CONFIG.robot_start_position[1])
        self.rotation = CONFIG.robot_start_rotation

        # Robot size (rectangular)
        self.width = float(CONFIG.robot_width)
        self.height = float(CONFIG.robot_height)

        # Define the outline of the robot as a polygon
        self.outline = CONFIG.robot_outline

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

        # Import the list of motors from the config file
        self.motors = CONFIG.motors

        # Import the list of drives from the config file
        self.drives = CONFIG.drives

        # Import the list of sensors from the config file
        self.sensors = CONFIG.sensors

        # All devices
        self.devices = self.motors | self.drives | self.sensors


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
        outline_global = [point.rotate(self.rotation) for point in self.outline]

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
        for device in self.devices.values():
            device.pos_update(self.position, self.rotation)
            device.update_outline()

    def draw_devices(self, canvas):
        '''
        Draws all devices on the robot onto the canvas unless marked otherwise.
        '''

        for device in self.devices.values():
            if device.visible:
                device.draw(canvas)
                if device.visible_measurement:
                    device.draw_measurement(canvas)

    def move_manual(self, keypress, walls):
        '''Determine the direction to move & rotate the robot based on keypresses.'''

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

        # Teleportation test
        # if keypress[K_t]:
        #    teleport_success = self.teleport(10, 10, 0, walls)
        #    if not teleport_success:
        #        print("Teleport failed due to collision.")

        # Move the robot
        self.move(move_vector, rotation, walls)

    def move_from_command(self, walls):
        '''Move the robot based on all the movement "stored" in the drives'''

        move_vector = pm.Vector2(0, 0)
        rotation = 0
        for drive in self.drives.values():
            # Get the movement amount from the drive, incrementing odometers
            if drive.move_buffer == 0:
                continue
            movement = drive.move_update()
            move_vector += movement[0]
            rotation += movement[1]

        # Move the robot
        self.move(move_vector, rotation, walls)

    def move(self, velocity, rotation, walls):
        '''Moves the robot, checking for collisions.'''
        # Update robot position
        self.position += pm.Vector2.rotate(velocity, self.rotation)
        self.rotation += rotation
        self.update_outline()

        # Reset the position if a collision is detected
        collisions = self.check_collision_walls_fast(walls)
        if collisions:
            self.position -= pm.Vector2.rotate(velocity, self.rotation)
            self.rotation -= rotation
            self.update_outline()

    def teleport(self, x, y, angle, walls):
        '''Attempts to teleport the robot to a location,
        returns True if successful
        if collision, reverts to previous location and returns False'''

        original_position = [self.position, self.rotation]

        self.position = pm.Vector2(x, y)
        self.rotation = angle
        self.update_outline()
        print(CONFIG.maze_dim_x, CONFIG.maze_dim_y)

        # Returns False if the selected position is outside of the bounds of the map
        if not (0 < self.position.x < CONFIG.maze_dim_x and 0 < self.position.y < CONFIG.maze_dim_y):
            self.position = original_position[0]
            self.rotation = original_position[1]
            self.update_outline()
            return False

        # Returns True if the robot isn't inside a block and if there's no intersection with walls.
        if not utilities.in_block(self.position) and not self.check_collision_walls_fast(walls):
            return True
        else:
            self.position = original_position[0]
            self.rotation = original_position[1]
            self.update_outline()
            return False

    def stop_drives(self):
        '''Stops all drives from moving, used as an emergency stop.'''
        for drive in self.drives.values():
            drive.move_buffer = 0

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

    def check_collision_walls_fast(self, walls: list)->bool:
        '''
        Checks for a collision between the robot's perimeter segments
        and a set of wall line segments.
        '''

        # Loop through all the robot outline line segments, checking for collisions
        for segment_bot in self.outline_global_segments:
            for segment_wall in walls:
                collides = utilities.check_collision_fast(
                    segment_bot, segment_wall
                )  # bool value
                if collides:
                    return True

        return False



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
                responses.append([cmd[0], target_device.simulate(value, environment)])
            else:
                if cmd[0] == 'xx':
                    self.stop_drives()
                    responses.append([cmd[0], 'DRIVE STOP'])
                else:
                    print('Target device ' + cmd[0] + ' not found.')
                    responses.append([cmd[0], 'Not Found'])

        return responses
