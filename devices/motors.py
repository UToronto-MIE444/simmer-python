'''
Defines a SimMeR device representing a motor & wheel.

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
from devices.device import Device

class MotorSimple(Device):
    '''Defines a basic motor & wheel'''

    def __init__(self, d_id: str, position: list, rotation: float, visible: bool):
        '''Initialization'''

        # Call super initialization
        super().__init__(self, d_id, position, rotation, visible)

        # Device type (i.e. "motor" or "sensor")
        self.d_type = 'motor'

        # Device outline position
        self.outline = [
            pygame.math.Vector2(-0.5, -0.5),
            pygame.math.Vector2(0, 1),
            pygame.math.Vector2(0.5, -0.5)
        ]

        # Display color
        self.color = (0, 255, 0)

        # Display thickness
        self.outline_thickness = 0.25

    def simulate(self, value: float):
        if value:
            return str(value) + '_response'
        else:
            return value