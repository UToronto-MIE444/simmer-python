'''
A blank template file that can be used to create new types of SimMeR devices.
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

class Template(Device):
    '''Defines a new device.'''

    def __init__(self, info: dict):
        '''Initialization'''

        # Call super initialization
        super().__init__(info['id'], info['position'], info['rotation'], info['visible'])

        # Device type (i.e. "drive", "motor", or "sensor")
        self.d_type = ''

        # A name for the device
        self.name = ''

        # Device outline
        self.outline = info.get('outline', [
            pm.Vector2(-0.5, -0.5),
            pm.Vector2(0, 1)
        ])

        # Display color
        self.color = info.get('color', (0, 255, 0))

        # Display thickness
        self.outline_thickness = info.get('outline_thickness', 0.25)


    def simulate(self, value: float, environment: dict):
        '''
        This defines what the device does when it is called by a command.
        It should return a value of some sort to the localization and control code.
        '''
        return 0

    def update(self, environment: dict):
        '''
        This function defines what the device does on every frame.
        It should not return anything, only update the devices self variables.
        '''
        pass
