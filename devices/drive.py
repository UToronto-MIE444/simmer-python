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
import pygame
from devices.device import Device
# import config.config as CONFIG

class Drive(Device):
    '''
    Defines a component of the robot's drive system. This is an abstract class that
    '''

    def __init__(self, d_id: str, motors: list, motor_directions: list):
        '''Initialization'''

        # Call super initialization
        # Because the drive device is abstract, hardcode position and rotation as 0, never display
        super().__init__(d_id, [0,0], 0, False)

        # Device type (i.e. "drive", "motor", or "sensor")
        self.d_type = 'drive'

        # Verify that the list of motors and the number of directions provided are equal
        if not len(motors) == len(motor_directions):
            raise Exception('Lists "motors" and "motor_directions" must be the same length')

        # Device outline - use minimal points since the device is abstract and won't be drawn
        self.outline = [
            pygame.math.Vector2(0, 1),
            pygame.math.Vector2(0, -1)
        ]

        # Motors to activate when command received
        self.motors = motors                        # Motor objects
        self.motor_directions = motor_directions    # Directions for each motor (+1 or -1)

        # Simulation parameters
        self.direction_default = 1  # +1: drive should trigger motors to move "forward", -1: "backward"


    def simulate(self, value: float, environment: dict):
        '''
        Tells the robot to move in a direction, unless it is already moving.
        '''
        ROBOT = environment.get('ROBOT', False)
        MAZE = environment.get('MAZE', False)
        BLOCK = environment.get('BLOCK', False)

        # Get all the motors
        all_motors = []
        for motor in ROBOT.motors:
            all_motors.append(motor)

        # Refuse the movement command if the robot is currently moving
        is_moving = False
        for motor in all_motors:
            if motor.move_buffer:
                is_moving = True

        if is_moving:
            return math.nan

        # Tell the correct motors to move
        for (motor, direction) in zip(self.motors, self.motor_directions):
            motor.move_buffer = direction * value

        # Return "inf" if the command is accepted and acknowledged
        return math.inf
