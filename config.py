'''
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

class Config:
    '''This class stores the configuration information for the simulator'''
    def __init__(self):
        self.foldername = 'config'
        self.drive_filename = 'drive.csv'
        self.maze_filename = 'maze.csv'
        self.robot_filename = 'robot.csv'
        self.sensors_filename = 'sensors.csv'

        # Simulation control information
        self.sim = True                 # Use the simulator (True) or connect to robot via blueteooth (False)
        self.step_time = 0              # Pause time between the algorithm executing commands

        # Bluetooth Serial Connection Constants
        self.comport_num = 6            # Bluetooth serial comport number to connect to
        self.comport_baud = 9600        # Bluetooth serial baudrate

        # Robot and block information
        self.start_position = [9.5, 42] # Robot starting location
        self.start_rotation = 0         # Robot starting rotation
        self.block_position = [25, 41]  # Block starting location
        self.block_size = 3             # Block side length in inches

        # Drive information
        self.num_segments = 10          # Number of movement segments
        self.strength = [0.05, 1]	    # How intense the random drive bias is, if enabled

        # Control Flags and Setup
        self.rand_error = True          # Use either true random error generator (True) or repeatable error generation (False)
        self.error_seed = 5489          # Seed for random error (used if rand_error is False)
        self.rand_bias = True           # Use a randomized, normally distributed set of drive biases

        # Plotting Flags
        self.plot_robot = True          # Plot the robot as it works its way through the maze
        self.plot_sense = True          # Plot sensor interactions with maze, if relevant

        # Maze size information
        self.wall_segment_length = 12   # Length of maze wall segments (inches)
        self.floor_segment_length = 3   # Size of floor pattern squares (inches)

        # Graphics information
        self.ppi = 12                   # Number of on-screen pixels per inch on display
        self.border_pixels = self.floor_segment_length * self.ppi   # Size of the border surrounding the maze area
        self.wall_thickness = 0.25      # Thickness to draw wall segments, in inches
        self.wall_color = (255, 0, 0)   # Tuple with wall color in (R,G,B) format

    def set_border(self, pixels):
        '''Sets the display border around the maze'''
        self.border_pixels = pixels
