'''
Defines a SimMeR device representing a compass.
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
import utilities

class Compass(Device):
    '''Defines a compass that allows for measurement of rotation.'''

    def __init__(self, info: dict):
        '''Initialization'''

        # Call super initialization
        super().__init__(info['id'], [0, 0], 0, info['visible'])

        # Device type (i.e. "drive", "motor", or "sensor")
        self.d_type = 'sensor'
        self.name = 'compass'

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
        self.error = info.get('error', 0.2) # Error when updating the gyroscope value
        self.bias = info.get('bias', 0.1)   # Bias that the compass has (deg)


    def simulate(self, value: float, environment: dict):
        '''Returns the odometer value.'''
        compass = self.rotation_global + self.bias
        compass_error = compass + utilities.add_error(360, self.error)
        return compass_error % 360
