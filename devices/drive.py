'''
Defines a SimMeR device representing a robot's drive.
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
import pygame.math as pm
from devices.device import Device
import utilities
import config as CONFIG

class Drive(Device):
    '''
    Defines a component of the robot's drive system. This is an abstract class that
    '''

    def __init__(self, info: dict):
        '''Initialization'''

        # Call super initialization
        # Because the drive device is abstract, hardcode position and rotation as 0, never display
        super().__init__(info['id'], info.get('position', [0, 0]), info.get('rotation', 0), info.get('visible', False))

        # Device type (i.e. "drive", "motor", or "sensor")
        self.d_type = 'drive'
        self.name = 'drive'

        # Verify that the list of motors and the number of directions provided are equal
        if len(info['motors']) != len(info['motor_direction']):
            raise RuntimeError('Lists "motors" and "motor_direction" must be the same length')

        # Device outline - use minimal points since the device is abstract and won't be drawn
        self.outline = info.get('outline', [
            pm.Vector2(0, 1),
            pm.Vector2(0, -1)
        ])

        # Movement values for each direction when this drive command is executed
        # ONLY ONE OF THESE TWO should be non-zero for each drive
        velocity = info.get('velocity', [0, 0])
        ang_velocity = info.get('ang_velocity', 0)
        self.velocity = pm.Vector2(velocity[0] / CONFIG.frame_rate, # inch/frame
                                   velocity[1] / CONFIG.frame_rate) # inch/frame
        self.rotation_speed =      ang_velocity / CONFIG.frame_rate # deg/frame

        # Get the unit vector of the velocity and angular velocity (the direction the robot will move)
        if self.velocity != pm.Vector2(0, 0):
            self.velocity_direction = self.velocity.normalize()
        else:
            self.velocity_direction = self.velocity

        if self.rotation_speed != 0:
            self.rotation_normalize = self.rotation_speed/self.rotation_speed
        else:
            self.rotation_normalize = 0

        # Motors whose odometers should be incremented when the drive is active
        self.motors = info['motors']

        # Amount to increment odometers (in inches) for each drive movement unit
        # For linear movement, drive units are inches, for rotational movement, units are degrees
        self.motor_direction = info['motor_direction']

        # Get the odometer multipliers
        self.odometer_multiplier = self._get_odometer_multiplier(info['motors'], info['motor_direction'])

        # Error and bias
        default = {'x':0, 'y':0, 'rotation':0}

        self.error_linear =  [info.get('error', default).get('x', 0),
                              info.get('error', default).get('y', 0)]
        self.error_rotation = info.get('error', default).get('rotation', 0)

        self.bias_linear =   [info.get('bias', default).get('x', 0),
                              info.get('bias', default).get('y', 0)]
        self.bias_rotation =  info.get('bias', default).get('rotation', 0)

        # Movement buffer (to split a movement command into multiple frames)
        self.move_buffer = 0


    def _get_odometer_multiplier(self, motors, motor_direction):
        '''
        For each motor, calculate the amount that 1 unit of movement (linear inch or
        rotational radian) for this drive will add to its odometer reading. Only active motors
        will be incremented, and motors not angled in the direction of motion are assumed to
        slip the necessary amount to get appropriate motion in the defined direction.
        '''
        odometer_multiplier = []
        for (motor, direction) in zip(motors, motor_direction):

            # Calculate the multiplier for linear motion
            if self.velocity.length():
                # Increase due to off-angle wheel slippage
                angle = math.radians(self.velocity_direction.angle_to(motor.point_vector))
                slip_compensation = abs(math.cos(angle))
                # DISTANCE_VALUE * mDir / slippage
                multiplier = direction / slip_compensation

            # Calculate the multiplier for rotational motion
            elif self.rotation_speed:
                ideal_rotation_direction = motor.position.rotate(90)
                # Increase due to off-angle wheel slippage
                angle = math.radians(ideal_rotation_direction.angle_to(motor.point_vector))
                slip_compensation = abs(math.cos(angle))
                # DEG_VALUE/360 * 2*pi*r * mDir / slippage
                multiplier = 1/360 * 2*math.pi*motor.position.length() * direction / slip_compensation

            # If neither present, set to 0
            else:
                multiplier = 0

            # Only one of these should ever be non-zero at a time, so we can add both together
            odometer_multiplier.append(multiplier)

        return odometer_multiplier


    def simulate(self, value: float, environment: dict):
        '''
        Tells the robot to move in a direction, unless it is already moving.
        '''
        ROBOT = environment.get('ROBOT', False)

        # Refuse the movement command if the robot is currently moving
        for drive in ROBOT.drives.values():
            if drive.move_buffer:
                return False

        # Add errors
        error_total = 0
        for v, e in zip(self.velocity_direction, self.error_linear):
            error_total += v*e
        if self.rotation_normalize:
            error_total += self.rotation_normalize * self.error_rotation
        value_error = utilities.add_error(value, error_total)
        # print(value, value_error)

        # Increment the movement buffer
        self.move_buffer = value_error

        # Return "inf" if the command is accepted and acknowledged
        return True


    def move_update(self):
        '''
        Returns the amount the drive should move based on its speed and the
        remaining movement buffer. Also updates the odometer sensor and decrements
        the movement buffer.
        '''

        # Clamp the amount to move to smaller of the motor speed and the remaining movement buffer
        # Add rotation and velocity because one should always be zero
        if self.move_buffer >= 0:
            move_amount = min(self.move_buffer, self.rotation_speed + self.velocity.length())
        else:
            move_amount = max(self.move_buffer, -(self.rotation_speed + self.velocity.length()))

        # Update the odometer value
        for (motor, increment) in zip(self.motors, self.odometer_multiplier):
            motor.odometer += move_amount * increment

        # Decrement the movement buffer with the amount the drive moved
        self.move_buffer -= move_amount

        # Calculate how much to move in each direction based on this drive
        rotation = 0
        move_vector = self.velocity_direction * move_amount
        if self.rotation_speed:
            rotation = move_amount

        # Add bias and error to the drive
        move_vector_error = [move_vector[0] + move_amount * self.bias_linear[0],
                             move_vector[1] + move_amount * self.bias_linear[1]]
        rotation_error =     rotation       + move_amount * self.bias_rotation

        return [move_vector_error, rotation_error]
