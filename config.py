'''
This class stores the configuration information for the simulator.

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

import numpy as np

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

# Robot and block information
start_position = [8, 40]    # Robot starting location
start_rotation = np.pi / 6  # Robot starting rotation
robot_width = 6             # Robot width in inches
robot_height = 6            # Robot height in inches
block_position = [25, 41]   # Block starting location
block_size = 3              # Block side length in inches

# Drive information
num_segments = 10           # Number of movement segments
strength = [0.05, 1]	    # How intense the random drive bias is, if enabled

# Control Flags and Setup
rand_error = True           # Use either true random error generator (True) or repeatable error generation (False)
error_seed = 5489           # Seed for random error (used if rand_error is False)
rand_bias = True            # Use a randomized, normally distributed set of drive biases

# Plotting Flags
plot_robot = True           # Plot the robot as it works its way through the maze
plot_sense = True           # Plot sensor interactions with maze, if relevant

# Maze size information
wall_segment_length = 12    # Length of maze wall segments (inches)
floor_segment_length = 3    # Size of floor pattern squares (inches)

# Graphics information
ppi = 12                    # Number of on-screen pixels per inch on display
border_pixels = floor_segment_length * ppi  # Size of the border surrounding the maze area

wall_thickness = 0.25       # Thickness to draw wall segments, in inches
wall_color = (255, 0, 0)    # Tuple with wall color in (R,G,B) format

robot_thickness = 0.25      # Thickness to draw robot perimeter, in inches
robot_color = (0, 0, 255)   # Tuple with robot perimeter color in (R,G,B) format
