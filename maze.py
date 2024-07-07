'''
This file defines the maze object in SimMeR.
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

import sys
import numpy as np
import pygame
import shapely as shp
import config as CONFIG
import utilities


class Maze:
    '''This class represents the maze/environment'''
    def __init__(self):

        self.size_y = 0
        self.size_x = 0

        self.wall_squares = []
        self.walls = []
        self.reduced_walls = []
        self.floor_tiles = []
        self.floor_tile_colors = 0
        self.floor_rect_black = []
        self.floor_rect_white = []
        self.floor_white_poly = 0

    def import_walls(self):
        '''Imports the walls from a csv file and sets up lines representing them'''

        wall_map = np.array(CONFIG.walls)
        dim_y = np.size(wall_map, 0)
        dim_x = np.size(wall_map, 1)

        self.size_y = CONFIG.maze_dim_y
        self.size_x = CONFIG.maze_dim_x

        # Outer maze dimensions
        self.wall_squares.append([
            [[0, 0], [dim_x, 0]],
            [[dim_x, 0], [dim_x, dim_y]],
            [[dim_x, dim_y], [0, dim_y]],
            [[0, dim_y], [0, 0]]
            ])

        for ct_x in range(0, dim_x):
            for ct_y in range(0, dim_y):
                if wall_map[ct_y, ct_x] == 0:
                    self.wall_squares.append([
                        [[ct_x, ct_y], [ct_x+1, ct_y]],
                        [[ct_x+1, ct_y], [ct_x+1, ct_y+1]],
                        [[ct_x+1, ct_y+1], [ct_x, ct_y+1]],
                        [[ct_x, ct_y+1], [ct_x, ct_y]]
                        ])

        # Convert to length
        self.wall_squares = [[[[scalar * CONFIG.wall_segment_length for scalar in point]
                               for point in line]
                              for line in square]
                             for square in self.wall_squares]

        # Flattens list of walls, removes unnecessary walls
        self.walls= [wall for wallsquare in self.wall_squares for wall in wallsquare]
        self.reduced_walls = utilities.optimize_walls(self.walls)

    def draw_walls(self, canvas):
        '''Draws the maze walls onto the screen'''

        # Graphics
        THICKNESS = int(CONFIG.wall_thickness * CONFIG.ppi)
        COLOR = CONFIG.wall_color

        for line in self.reduced_walls:
                start = [scalar * CONFIG.ppi + CONFIG.border_pixels for scalar in line[0]]
                end = [scalar * CONFIG.ppi + CONFIG.border_pixels for scalar in line[1]]
                pygame.draw.line(canvas, COLOR, start, end, THICKNESS)

    def generate_floor(self):
        '''Generates the floor of the maze'''

        if not self.reduced_walls:
            sys.exit('Walls must be imported before a floor pattern is generated.')

        # Get the number of floor checker points
        dim_x = int(self.size_x / CONFIG.floor_segment_length)
        dim_y = int(self.size_y / CONFIG.floor_segment_length)

        # Create the floor tiles
        self.floor_tile_colors = np.floor(np.random.random(dim_y * dim_x)*2) * 255

        floor_tiles = []
        for ct_x in range(0, dim_x):
            for ct_y in range(0, dim_y):
                floor_tiles.append([
                    [ct_x, ct_y], [ct_x+1, ct_y], [ct_x+1, ct_y+1], [ct_x, ct_y+1]
                    ])

        # Convert to length
        self.floor_tiles = [[[scalar * CONFIG.floor_segment_length for scalar in point]
                             for point in tile]
                            for tile in floor_tiles]

        # Create an array of rectangle objects for drawing
        width = CONFIG.floor_segment_length * CONFIG.ppi
        floor_white_polys = []
        for (tile, color) in zip(self.floor_tiles, self.floor_tile_colors.tolist()):
            left = tile[0][0] * CONFIG.ppi + CONFIG.border_pixels
            top = tile[0][1] * CONFIG.ppi + CONFIG.border_pixels
            tile_rect = pygame.Rect(left, top, width, width)

            # Append the rectangles to floor objects. Create shapely polygons.
            if color:
                self.floor_rect_white.append(tile_rect)
                floor_white_polys.append(shp.Polygon(tile))
            else:
                self.floor_rect_black.append(tile_rect)

        # Create a multipolygon object
        self.floor_white_poly = shp.MultiPolygon(floor_white_polys)

        return True

    def draw_floor(self, canvas):
        '''Draws the maze floor'''
        for white_tile in self.floor_rect_white:
            pygame.draw.rect(canvas, (255, 255, 255), white_tile)
        for black_tile in self.floor_rect_black:
            pygame.draw.rect(canvas, (0, 0, 0), black_tile)
