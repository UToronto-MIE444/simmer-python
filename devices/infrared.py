'''
Defines a SimMeR device representing a downward-facing ultrasonic sensor.
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
import shapely as shp
from devices.device import Device
import config as CONFIG
import utilities

class Infrared(Device):
    '''Defines a downward-facing infrared sensor used to detect the floor pattern.'''

    def __init__(self, info: dict):
        '''Initialization'''

        # Call super initialization
        super().__init__(info['id'], info['position'], info['rotation'], info['visible'])

        # Device type (i.e. "drive", "motor", or "sensor")
        self.d_type = 'sensor'
        self.name = 'infrared'

        # Device outline position
        self.outline = info.get('outline', [
            pm.Vector2(-0.5, -0.5),
            pm.Vector2(-0.5, 0.5),
            pm.Vector2(0.5, 0.5),
            pm.Vector2(0.5, -0.5)
        ])

        # Height
        self.height = info.get('height', 3)

        # Display color
        self.color = info.get('color', (0, 0, 255))

        # Display thickness
        self.outline_thickness = info.get('outline_thickness', 0.25)

        # Display measurement when simulating
        self.visible_measurement = info.get('visible_measurement', False)
        self.visible_measurement_time = info.get('visible_measurement_time', 0.5)    # Measurement time on screen (s)
        self.visible_measurement_buffer = 0

        # Simulation parameters
        self.fov = info.get('fov', 60)              # Field of view angle
        self.view_r = self.height * math.cos(math.radians(self.fov/2))
        self.view_circle = shp.Point(self.position_global[0], self.position_global[1]).buffer(self.view_r)
        self.threshold = info.get('threshold', 0.8)

        self.error_pct = info.get('error', 0.02)    # Percent error (0-1)

    def draw_measurement(self, canvas):
        '''Draw ultrasonic sensor rays on the canvas'''

        # If the measurement should be displayed
        if self.visible_measurement_buffer:
            # Graphics options
            THICKNESS = int(CONFIG.ppi*0.125)
            COLOR = (255, 255, 0)

            # Circle parameters
            center = [value*CONFIG.ppi + CONFIG.border_pixels for value in self.position_global]
            radius = self.view_r * CONFIG.ppi

            pygame.draw.circle(canvas, COLOR, center, radius, THICKNESS)

            # Decrement the buffer
            self.visible_measurement_buffer -= 1

    def simulate(self, value: float, environment: dict):
        '''
        Simulates the performance of the ultrasonic sensor.
        '''

        # Update the measurement display buffer
        self.visible_measurement_buffer = int(self.visible_measurement_time * CONFIG.frame_rate)

        # Simulate the performance
        MAZE = environment.get('MAZE', False)

        self.view_circle = shp.Point(self.position_global[0], self.position_global[1]).buffer(self.view_r)
        area = math.pi * self.view_r * self.view_r

        floor = MAZE.floor_white_poly

        overlap = self.view_circle.intersection(floor)

        intersect_percent = overlap.area/area

        intersect_error = utilities.add_error(intersect_percent, self.error_pct, [0,1])

        if intersect_error >= self.threshold:
            return True
        else:
            return False
