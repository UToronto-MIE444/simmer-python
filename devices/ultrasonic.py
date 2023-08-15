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

import numpy as np
import pygame
from devices.device import Device
import config.config as CONFIG
from utilities import check_collision_walls as collision

class Ultrasonic(Device):
    '''Defines an ultrasonic sensor.'''

    def __init__(self, d_id: str, position: list, rotation: float, visible: bool):
        '''Initialization'''

        # Call super initialization
        super().__init__(self, d_id, position, rotation, visible)

        # Device type (i.e. "motor" or "sensor")
        self.d_type = "sensor"

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
        self.beamwidth = 15*np.pi/180   # Beamwidth of the ultrasonic sensor
        self.num_rays = 11              # Number of rays to test
        self.max_range = 433            # Maximum range in inches

        self._define_rays()

    def _define_rays(self):
        '''Define the rays used to get the ultrasonic distance.'''

        rays = []
        for ct in range(0, self.num_rays):
            # Calculate the angle of each ray
            angle_ray = ((ct - (self.num_rays-1)/2) / self.num_rays) * self.beamwidth
            angle_ray_a = angle_ray + self.rotation_a

            # Calculate the start and end points of each ray
            direction = pygame.math.Vector2(0,self.max_range)
            ray_end = pygame.math.Vector2.rotate_rad(direction, angle_ray_a) + self.position_a

            # Append the calculated rays
            rays.append([self.position_a, ray_end])

        return rays


    def simulate(self, value: float):
        '''
        Simulates the performance of an ultrasonic sensor.

        Response data format
        [0:7] - Eight byte double
        '''

        rays = self._define_rays()


    def draw_measurement(self, canvas):
        '''Draw ultrasonic sensor rays on the canvas'''

        # Update positions. Might need to be moved later to reduce cpu cycles
        self.rays = self._define_rays()

        # Graphics options
        thickness = int(CONFIG.ppi*0.125)
        color = (0, 0, 255)

        # Draw the lines on the canvas
        for ray in self.rays:
            start = [point*CONFIG.ppi + CONFIG.border_pixels for point in ray[0]]
            end = [point*CONFIG.ppi + CONFIG.border_pixels for point in ray[1]]
            pygame.draw.line(canvas, color, start, end, thickness)