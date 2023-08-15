'''
Defines a SimMeR device representing an ultrasonic sensor.

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
import statistics
import pygame
from devices.device import Device
import config.config as CONFIG
import utilities

class Ultrasonic(Device):
    '''Defines an ultrasonic sensor.'''

    def __init__(self, d_id: str, position: list, rotation: float, visible: bool):
        '''Initialization'''

        # Call super initialization
        super().__init__(self, d_id, position, rotation, visible)

        # Device type (i.e. "motor" or "sensor")
        self.d_type = 'sensor'

        # Device outline position
        self.outline = [
            pygame.math.Vector2(-1, -0.5),
            pygame.math.Vector2(-1, 0.5),
            pygame.math.Vector2(1, 0.5),
            pygame.math.Vector2(1, -0.5)
        ]

        # Display color
        self.color = (0, 0, 255)

        # Display thickness
        self.outline_thickness = 0.25

        # Simulation parameters
        self.beamwidth = 15*math.pi/180   # Beamwidth of the ultrasonic sensor
        self.num_rays = 11              # Number of rays to test
        self.max_range = 433            # Maximum range in inches

        self.rays = self._define_rays() # Define the initial rays, without detecting collisions
        self.ray_lengths = [self.max_range for item in self.rays]   # The length of the rays

    def _define_rays(self):
        '''Define the rays used to get the ultrasonic distance.'''

        rays = []
        for ct in range(0, self.num_rays):
            # Calculate the angle of each ray
            angle_ray = ((ct - (self.num_rays-1)/2) / self.num_rays) * self.beamwidth
            angle_ray_global = angle_ray + self.rotation_global

            # Calculate the start and end points of each ray
            direction = pygame.math.Vector2(0,self.max_range)
            ray_end = pygame.math.Vector2.rotate_rad(direction, angle_ray_global) + self.position_global

            # Append the calculated rays
            rays.append([self.position_global, ray_end])

        return rays

    def draw_measurement(self, canvas):
        '''Draw ultrasonic sensor rays on the canvas'''

        # Graphics options
        thickness = int(CONFIG.ppi*0.125)
        color = (0, 0, 255)

        # Draw the lines on the canvas
        for ray in self.rays:
            start = [point*CONFIG.ppi + CONFIG.border_pixels for point in ray[0]]
            end = [point*CONFIG.ppi + CONFIG.border_pixels for point in ray[1]]
            pygame.draw.line(canvas, color, start, end, thickness)

    def simulate(self, value: float, environment: dict):
        '''
        Simulates the performance of an ultrasonic sensor.

        Response data format
        [0:7] - Eight byte double
        '''
        ROBOT = environment.get('ROBOT', False)
        MAZE = environment.get('MAZE', False)
        BLOCK = environment.get('BLOCK', False)

        rays = self._define_rays()
        ray_lengths = [self.max_range for item in rays]

        for ct, ray in enumerate(rays):
            for square in MAZE.wall_squares:
                for segment_wall in square:
                    collision_points = utilities.collision(ray, segment_wall)
                    if not collision_points:
                        pass
                    else:
                        rays[ct][1], ray_lengths[ct] = utilities.closest(self.position_global, collision_points)

        # Update stored variables
        self.rays = rays
        self.ray_lengths = ray_lengths

        # Build the value to return
        output = statistics.median(self.ray_lengths)

        return output
