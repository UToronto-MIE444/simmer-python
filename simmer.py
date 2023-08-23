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

# Imports
import numpy as np
import pygame
from maze import Maze
from robot import Robot
from interface.hud import Hud
from interface.communication import TCPServer
import config.config as CONFIG
import utilities

### Initialization
print('SimMeR Loading...')

# Everything in comments needs to be replaced/replicated
'''

# Build Block
block = build_block(blocksize, block_center);

# Import Sensor Loadout and Positions
sensor = import_sensor;

# Import Drive information
drive = import_drive;

# Initialize integration-based sensor values
gyro_num = [];
odom_num = [];
for ct = 1:size(sensor.id)
    if strcmp('gyro', sensor.id{ct}(1:end-1))
        gyro_num = [gyro_num ct];
    end
    if strcmp('odom', sensor.id{ct}(1:end-1))
        odom_num = [odom_num ct];
    end
end

# Populate the gyroscope and odometer sensor variables
gyro = [gyro_num', sensor.err(gyro_num'), zeros(size(gyro_num))'];
odom = [odom_num', sensor.err(odom_num'), zeros(size(odom_num))'];


## Act on initialization flags


# Randomize drive biases to verify algorithm robustness
if randbias
    drive = bias_randomize(drive, strength);
end

# Create the plot
if plot_robot

    # Block
    block_plot = patch(block(:,1),block(:,2), 'y');
    set(block_plot,'facealpha',.5)

end
'''

# Set random error seed
if not CONFIG.rand_error:
    np.random.seed(CONFIG.error_seed)

# Load maze walls and floor pattern
MAZE = Maze()
MAZE.import_walls()
MAZE.generate_floor()
CANVAS_WIDTH = MAZE.size_x * CONFIG.ppi + CONFIG.border_pixels * 2
CANVAS_HEIGHT = MAZE.size_y * CONFIG.ppi + CONFIG.border_pixels * 2

# Load robot
ROBOT = Robot()

# Create a copy of the environment objects to pass to simulation functions
environment = {'ROBOT': ROBOT, 'MAZE': MAZE}

# Load the Heads Up Display
HUD = Hud()

# Load TCP Communication
COMM = TCPServer()
COMM.start()

# Initialize graphics
pygame.init()
canvas = pygame.display.set_mode([CANVAS_WIDTH, CANVAS_HEIGHT])

### Main Loop ###
RUNNING = True
try:
    while RUNNING:

        ##########################
        ##### USER INTERFACE #####
        ##########################
        # Check for and act on keyboard input
        game_events = pygame.event.get()
        RUNNING = HUD.check_input(game_events)
        keypress = pygame.key.get_pressed()

        # Get the command information from the tcp buffer
        cmds = COMM.get_buffer_rx()

        ################################################
        ##### ROBOT AND DEVICE UPDATES AND ACTIONS #####
        ################################################
        # Act on commands and respond
        if cmds:
            responses = ROBOT.command(cmds, environment)
            COMM.set_buffer_tx(responses)

        # Move the robot, either from keypress commands or from the movement buffers
        if True in keypress:
            ROBOT.move_manual(keypress, MAZE.wall_squares)
        else:
            ROBOT.move_from_command(MAZE.wall_squares)

        # Recalculate global positions of the robot and its devices
        ROBOT.update_outline()
        ROBOT.update_device_positions()

        # Manually simulate a specific sensor or sensors
        utilities.simulate_sensors(environment, ['u0'])

        # Update the sensors that need to be updated every frame
        for sensor in ROBOT.sensors.values():
            if callable(getattr(sensor, "update", None)):
                sensor.update()

        ###########################################
        ##### DRAW RELEVANT OBJECTS ON CANVAS #####
        ###########################################
        # Fill the background with the background color
        canvas.fill(CONFIG.background_color)

        # Draw the maze checkerboard pattern
        MAZE.draw_floor(canvas)

        # Draw the maze walls
        MAZE.draw_walls(canvas)

        # Draw the robot onto the maze
        ROBOT.draw(canvas)
        ROBOT.draw_devices(canvas)

        # Update the various HUD elements
        HUD.draw_frame_indicator(canvas)
        HUD.draw_keys(canvas, keypress)

        # Limit the framerate
        HUD.clock.tick(CONFIG.frame_rate)

        # Flip the display (update the canvas)
        pygame.display.flip()

except KeyboardInterrupt:
    pass

# Done! Time to quit.
print('Execution finished. Closing SimMeR.')
pygame.quit()
