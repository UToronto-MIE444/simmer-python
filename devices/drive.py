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
import config.config as CONFIG

class Drive(Device):
    '''
    Defines a component of the robot's drive system. This is an abstract class that
    '''

    def __init__(self, d_id: str, drive_velocity: list, motors: list, motor_direction: list):
        '''Initialization'''

        # Call super initialization
        # Because the drive device is abstract, hardcode position and rotation as 0, never display
        super().__init__(d_id, [0,0], 0, False)

        # Device type (i.e. "drive", "motor", or "sensor")
        self.d_type = 'drive'

        # Verify that the list of motors and the number of directions provided are equal
        if not len(motors) == len(motor_direction):
            raise Exception('Lists "motors" and "motor_direction" must be the same length')

        # Device outline - use minimal points since the device is abstract and won't be drawn
        self.outline = [
            pygame.math.Vector2(0, 1),
            pygame.math.Vector2(0, -1)
        ]

        # Movement values for each direction when this drive command is executed
        # Only one of these SHOULD be non-zero for each drive direction
        self.velocity = pygame.math.Vector2(drive_velocity[0] / CONFIG.frame_rate,  # inch/frame
                                            drive_velocity[1] / CONFIG.frame_rate)  # inch/frame
        self.rotation = drive_velocity[2] / CONFIG.frame_rate                       # rad/frame

        # Movement buffer (to split a movement command into multiple frames)
        self.move_buffer = 0

        # Motors whose odometers should be incremeneted
        self.motors = motors

        # Amount to increment odometers (in inches) for each drive movement unit
        # For linear movement, drive units are inches, for rotational movement, units are radians
        self.motor_direction = motor_direction

        # Get the unit vector of the velocity (the direction the robot will move)
        if not (self.velocity == pygame.math.Vector2(0,0)):
            velocity_direction = self.velocity.normalize()
        else:
            velocity_direction = self.velocity

        # For each motor, calculate the amount that 1 unit of movement (linear inch or rotational radian)
        # for this drive will add to its odometer reading. Only active motors will be incremented, and motors
        # not angled in the direction of motion are assumed to slip the necessary amount to get appropriate
        # motion in the defined direction.
        self.odometer_increment = []
        for (motor, direction) in zip(motors, motor_direction):
            # Calculate the multiplier for linear motion
            # Increase due to off-angle wheel slippage
            lin_compensation = math.cos(velocity_direction.angle_to(motor.point_vector))
            # DISTANCE_VALUE * mDir / slippage
            linear_multiplier = direction / lin_compensation

            # Calculate the multiplier for rotational motion
            ideal_rotation_direction = motor.position.rotate_rad(math.pi/2)
            # Increase due to off-angle wheel slippage
            rot_compensation = math.cos(ideal_rotation_direction.angle_to(motor.point_vector))
            # RADIAN_VALUE / (2*pi) * 2*pi*r / slippage
            rotation_multiplier = 1 / (2*math.pi) * 2*math.pi*motor.position.length() / rot_compensation

            # Only one of these should ever be non-zero at a time, so we can add both together and store
            self.odometer_increment.append(linear_multiplier + rotation_multiplier)


    def simulate(self, value: float, environment: dict):
        '''
        Tells the robot to move in a direction, unless it is already moving.
        '''
        ROBOT = environment.get('ROBOT', False)
        MAZE = environment.get('MAZE', False)
        BLOCK = environment.get('BLOCK', False)

        # Refuse the movement command if the robot is currently moving
        for drive in ROBOT.drives:
            if drive.move_buffer:
                return math.nan

        # Increment the movement buffer
        self.move_buffer = value

        # Return "inf" if the command is accepted and acknowledged
        return math.inf

    def move_update(self):
        '''
        Returns the distance the motor should move based on its speed and the
        remaining movement buffer. Also updates the odometer sensor and decrements
        the movement buffer.
        '''

        # Clamp the distance to move to smaller of the motor speed and the remaining movement buffer
        if self.move_buffer >= 0:
            move_distance = pygame.math.Vector3(min(self.move_buffer, self.velocity.x),
                                                min(self.move_buffer, self.velocity.y))
        else:
            move_distance = pygame.math.Vector3(max(self.move_buffer, self.velocity.x),
                                                max(self.move_buffer, self.velocity.y))

        # Update the odometer value
        for motor in self.motors:
            pass

        # Decrement the movement buffer with the distance the motor was rotated
        self.move_buffer -= move_distance

        return move_distance

    def update(self):
        '''
        Updates the position and/or rotation of the robot.
        '''

        # Transformational (linear) Movement
        if self.move_buffer >= 0:
            move_distance = min(self.move_buffer, self.speed/CONFIG.frame_rate)
        else:
            move_distance = max(self.move_buffer, -self.speed/CONFIG.frame_rate)

        # Initial position of the robot
