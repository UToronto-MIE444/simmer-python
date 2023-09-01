'''
This file stores the configuration information for the simulator.
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
import numpy as np
import pygame.math as pm
from devices.motors import MotorSimple
from devices.ultrasonic import Ultrasonic
from devices.gyroscope import Gyroscope
from devices.compass import Compass
from devices.infrared import Infrared
from devices.drive import Drive

foldername = 'config'
drive_filename = 'drive.csv'
maze_filename = 'maze.csv'
robot_filename = 'robot.csv'
sensors_filename = 'sensors.csv'

# Simulation control information
sim = True                  # Use the simulator (True) or connect to robot via blueteooth (False)
step_time = 0               # Pause time between the algorithm executing commands

# Bluetooth Serial Connection Constants
comport_num = 6             # Bluetooth serial comport number to connect to
comport_baud = 9600         # Bluetooth serial baudrate

# Network configuration
host = '127.0.0.1'
port_rx = 61200
port_tx = 61201
timeout = 180
str_encoding = 'utf-8'

# Robot and Block information
start_position = [8, 40]    # Robot starting location (in)
start_rotation = 0          # Robot starting rotation (deg)
robot_width = 6             # Robot width in inches
robot_height = 6            # Robot height in inches
block_position = [66, 5]   # Block starting location
block_rotation = 0          # Block rotation (deg)
block_size = 3              # Block side length in inches

# Drive information
num_segments = 10           # Number of movement segments
strength = [0.05, 1]	    # How intense the random drive bias is, if enabled

# Control Flags and Setup
rand_error = False          # Use either true random error generator (True) or repeatable error generation (False)
error_seed = 5489           # Seed for random error (used if rand_error is False)
rand_bias = True            # Use a randomized, normally distributed set of bias values for devices with bias

# Plotting Flags
plot_robot = True           # Plot the robot as it works its way through the maze
plot_sense = True           # Plot sensor interactions with maze, if relevant

# Maze size information
wall_segment_length = 12    # Length of maze wall segments (inches)
floor_segment_length = 3    # Size of floor pattern squares (inches)

# Graphics information
frame_rate = 60             # Target frame rate (Hz)
ppi = 16                    # Number of on-screen pixels per inch on display
border_pixels = floor_segment_length * ppi  # Size of the border surrounding the maze area

background_color = (43, 122, 120)

wall_thickness = 0.25       # Thickness to draw wall segments, in inches
wall_color = (255, 0, 0)    # Tuple with wall color in (R,G,B) format

robot_thickness = 0.25      # Thickness to draw robot perimeter, in inches
robot_color = (0, 0, 255)   # Tuple with robot perimeter color in (R,G,B) format

block_thickness = 0.25      # Thickness to draw robot perimeter, in inches
block_color = (127, 127, 0) # Tuple with robot perimeter color in (R,G,B) format



### DEVICE CONFIGURATION ###
# Motors
m0_info = {
    'id': 'm0',
    'position': [2, 0],
    'rotation': 0,
    'visible': True
}

m1_info = {
    'id': 'm0',
    'position': [-2, 0],
    'rotation': 0,
    'visible': True
}

motors = {
    'm0': MotorSimple(m0_info),
    'm1': MotorSimple(m1_info)
}

# Drives
w0_info = {
    'id': 'w0',
    'velocity': [0, 6],
    'ang_velocity': 0,
    'motors': [motors['m0'], motors['m1']],
    'motor_direction': [1, 1],
    'bias': {'x': 0, 'y': 0, 'rotation': 0.5},
    'error': {'x': 0.02, 'y': 0.05, 'rotation': 1}
}

d0_info = {
    'id': 'd0',
    'velocity': [6, 0],
    'ang_velocity': 0,
    'motors': [motors['m0'], motors['m1']],
    'motor_direction': [1, 1],
    'bias': {'x': 0, 'y': 0, 'rotation': 1},
    'error': {'x': 0.05, 'y': 0.02, 'rotation': 1}
}

r0_info = {
    'id': 'r0',
    'velocity': [0, 0],
    'ang_velocity': 120,
    'motors': [motors['m0'], motors['m1']],
    'motor_direction': [1, -1],
    'bias': {'x': 0, 'y': 0, 'rotation': 0.02},
    'error': {'x': 0.003, 'y': 0.003, 'rotation': 0.02}
}

drives = {
    'w0': Drive(w0_info),
    'r0': Drive(r0_info)
}

# Sensors
u0_info = {
    'id': 'u0',
    'position': [0, 3],
    'height': 2,
    'rotation': 0,
    'error': 0.02,
    'outline': [
        pm.Vector2(-1, -0.5),
        pm.Vector2(-1, 0.5),
        pm.Vector2(1, 0.5),
        pm.Vector2(1, -0.5)
    ],
    'visible': True,
    'visible_measurement': False
}

u1_info = {
    'id': 'u1',
    'position': [0, 1],
    'height': 6,
    'rotation': 0,
    'error': 0.02,
    'outline': [
        pm.Vector2(-1, -0.5),
        pm.Vector2(-1, 0.5),
        pm.Vector2(1, 0.5),
        pm.Vector2(1, -0.5)
    ],
    'visible': True,
    'visible_measurement': True
}

g0_info = {
    'id': 'u0',
    'position': [0, 0],
    'rotation': 0,
    'error': 0.02,
    'bias': 0.1,
    'visible': False
}

c0_info = {
    'id': 'c0',
    'position': [0, 0],
    'rotation': 0,
    'error': 0.02,
    'bias': 0.1,
    'visible': False
}

i0_info = {
    'id': 'i0',
    'position': [0, -1],
    'height': 1.5,
    'rotation': 0,
    'fov': 60,
    'threshold': 0.7,
    'error': 0.05,
    'bias': 0.1,
    'color': (127, 127, 127),
    'visible': True,
    'visible_measurement': True
}

sensors = {
    'u0': Ultrasonic(u0_info),
    'u1': Ultrasonic(u1_info),
    'g0': Gyroscope(g0_info),
    'c0': Compass(c0_info),
    'i0': Infrared(i0_info)
}

### TESTING AND DEBUG SETTINGS ###
simulate_list = ['u0', 'u1', 'i0']
