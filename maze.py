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

import numpy as np

class Maze:
    '''This class represents the maze/environment'''
    def __init__(self):
        self.walls = np.empty((1, 1))
        self.floor = np.array((1, 1))
        self.wall_squares = []
        self.floor_squares = []

    def import_walls(self, maze_filename):
        '''Imports the walls from a csv file and sets up lines representing them'''

        wall_map = np.loadtxt(maze_filename, delimiter=',', dtype=int)
        dim_y = np.size(wall_map, 0)
        dim_x = np.size(wall_map, 1)

        # Outer maze dimensions
        self.wall_squares.append(np.array([[0, 0], [dim_x, 0], [dim_x, dim_y], [0, dim_y], [0, 0]]))

        for ct_x in range(0, dim_x):
            for ct_y in range(0, dim_y):
                if wall_map[ct_y, ct_x] != 0:
                    self.wall_squares.append(np.array([
                        [ct_x, ct_y],
                        [ct_x+1, ct_y],
                        [ct_x+1, ct_y+1],
                        [ct_x, ct_y+1],
                        [ct_x, ct_y]
                        ]) * 12)    # convert from feet to inches

        # Generate a plot of the maze walls if specified in the config
