'''
Defines a SimMeR device representing a gyroscope.
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

import pygame.math as pm
from devices.device import Device
import config as CONFIG
import utilities

class Gyroscope(Device):
    '''Defines a gyroscope that allows for measurement of rotation.'''

    def __init__(self, info: dict):
        '''Initialization'''

        # Call super initialization
        super().__init__(info['id'], [0, 0], 0, info['visible'])

        # Device type (i.e. "drive", "motor", or "sensor")
        self.d_type = 'sensor'
        self.name = 'gyroscope'

        # Device outline position
        self.outline = info.get('outline', [
            pm.Vector2(-0.5, -0.5),
            pm.Vector2(0, 1)
        ])

        # Display color
        self.color = info.get('color', (0, 255, 0))

        # Display thickness
        self.outline_thickness = info.get('outline_thickness', 0.25)

        # Simulation parameters
        self.gyro = 0                               # gyroscope value (in degrees)
        self.rotation_true = [self.rotation_global, self.rotation_global]   # [Previous rotation, Current rotation] (deg)
        self.error = info.get('error', 0.2)         # Error when updating the gyroscope value
        self.bias = info.get('bias', 0.1)           # Bias that the gyroscope drifts with (deg/s)


    def simulate(self, value: float, environment: dict):
        '''Returns the odometer value.'''
        return self.gyro

    def update(self):
        '''Updates the gyroscope value based on the movement of the robot.'''

        # Update the previous and current rotations
        self.rotation_true[0] = self.rotation_true[1]
        self.rotation_true[1] = self.rotation_global

        # Add Error and update the device, wrap from 0 - 360 degrees
        change = self.rotation_true[1] - self.rotation_true[0] + self.bias/CONFIG.frame_rate
        self.gyro = (self.gyro + utilities.add_error(change, self.error)) % 360
