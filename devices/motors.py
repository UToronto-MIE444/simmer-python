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
import config.config as CONFIG

class MotorSimple(Device):
    '''Defines a basic motor & wheel'''

    def __init__(self, d_id: str, position: list, rotation: float, visible: bool):
        '''Initialization'''

        # Call super initialization
        super().__init__(d_id, position, rotation, visible)

        # Device type (i.e. "drive", "motor", or "sensor")
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

        # Simulation parameters
        self.speed = 1          # Speed in inches per second
        self.move_buffer = 0    # A buffer to indicate how much the motor should move before stopping
        self.odometer = 0       # Odometer movement

    def simulate(self, value: float, environment: dict):
        '''Returns the odometer value.'''
        return self.odometer

    def move_update(self, environment: dict):
        '''More work needed'''

        ROBOT = environment.get('ROBOT', False)
        MAZE = environment.get('MAZE', False)
        BLOCK = environment.get('BLOCK', False)

        # Clamp the distance to move to smaller of the motor speed and the remaining movement buffer
        if self.move_buffer >= 0:
            positive = True
            move_distance = min(self.move_buffer, self.speed/CONFIG.frame_rate)
        else:
            positive = False
            move_distance = max(self.move_buffer, -self.speed/CONFIG.frame_rate)

        # Here we need to call the robot's movement routine to calculate the total movement and rotation
        '''code goes here'''

        # Update the odometer value
        self.odometer += move_distance

        # Decrement the movement buffer with the distance the motor was rotated
        self.move_buffer -= move_distance
