'''
Defines the SimMeR Robot class.

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
import pygame
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_q,
    K_e
)
import config.config as CONFIG

class Robot():
    '''This class represents the robot'''

    def __init__(self):
        '''Initialize the robot class'''

        # Position information (stored in inches)
        self.position = pygame.math.Vector2(CONFIG.start_position[0], CONFIG.start_position[1])
        self.rotation = CONFIG.start_rotation

        # Robot size (rectangular)
        self.width = float(CONFIG.robot_width)
        self.height = float(CONFIG.robot_height)

        # Define the outline of the robot as a polygon
        self.outline = [
            pygame.math.Vector2(-self.width/2, -self.height/2),
            pygame.math.Vector2(-self.width/2,  self.height/2),
            pygame.math.Vector2( self.width/2,  self.height/2),
            pygame.math.Vector2( self.width/2, -self.height/2)
            ]

        self.outline_a = []
        self.outline_a_segments = []
        self.define_perimeter()

        # Is the robot currently colliding with a maze wall?
        self.collision = False

        # A trail of points where the robot has moved
        self.trail = [{
            "position": self.position,
            "rotation": self.rotation,
            "collision": self.collision
        }]

        # Import the list of devices from the config file
        self.devices = CONFIG.devices

    def append_trail(self):
        '''Appends current position information to the robot's trail'''

        self.trail.append({
            "position": self.position,
            "rotation": self.rotation,
            "collision": self.collision
        })

    def define_perimeter(self):
        '''Define the perimeter points of the robot, in inches, relative
        to the center point of the robot.'''

        # Rotate the outline
        outline_a = [point.rotate_rad(self.rotation) for point in self.outline]

        # Place the outline in the right location
        self.outline_a = [point + self.position for point in outline_a]

        # Convert the outline points to line segments
        segments = []
        for ct in range(-1, len(self.outline_a) - 1):
            segments.append((self.outline_a[ct], self.outline_a[ct+1]))

        self.outline_a_segments = segments

    def draw(self, canvas):
        '''Draws the robot outline on the canvas'''

        # Graphics
        THICKNESS = int(CONFIG.robot_thickness * CONFIG.ppi)
        COLOR = CONFIG.robot_color

        # Convert the outline from inches to pixels
        outline = [point * CONFIG.ppi + [CONFIG.border_pixels, CONFIG.border_pixels]
                   for point in self.outline_a]

        # Draw the polygon
        pygame.draw.polygon(canvas, COLOR, outline, THICKNESS)


    def check_collision(self):
        '''Check whether there is a collision between the robot and a wall'''

    def parse_command(self):
        '''Parse text string of commands and act on them'''

    def build_response(self):
        '''Builds a string response to send information back to the control algorithm'''

    def device_positions(self):
        '''Updates all the absolute positions of all the devices and their
        perimeters.'''

        for device in self.devices.values():
            device.pos_update(self.position, self.rotation)
            device.define_perimeter()

    def draw_devices(self, canvas):
        '''Draws all devices on the robot onto the canvas'''

        for device in self.devices.values():
            device.draw(canvas)

    def move_manual(self, keypress, walls):
        '''Move the robot manually with the keyboard'''

        velocity = pygame.math.Vector2(0, 0)
        rotation = 0

        # Forward/backward movement
        if keypress[K_w]:
            velocity += [0, 1/CONFIG.ppi]
        if keypress[K_s]:
            velocity += [0, -1/CONFIG.ppi]

        # Left/right movement
        if keypress[K_q]:
            velocity += [1/CONFIG.ppi, 0]
        if keypress[K_e]:
            velocity += [-1/CONFIG.ppi, 0]

        # Rotation
        if keypress[K_d]:
            rotation += np.pi/60
        if keypress[K_a]:
            rotation += -np.pi/60

        # Update robot position
        self.position += pygame.math.Vector2.rotate_rad(velocity, self.rotation)
        self.rotation += rotation
        self.define_perimeter()

        # Reset the position if a collision is detected
        collisions = self._check_collision(walls)
        if collisions:
            self.position -= pygame.math.Vector2.rotate_rad(velocity, self.rotation)
            self.rotation -= rotation
            self.define_perimeter()

    def _check_collision(self, wall_bounds):
        '''Checks for a collision between the robot and the maze walls.'''
        # Some code in this section from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

        def on_segment(p, q, r):
            # Calculates if a point q is on a line segment (p, r)

            if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
                (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
                return True
            else:
                return False

        def orientation(p, q, r):
            # Finds the orientation of an ordered triplet (p,q,r)
            # Returns the following values:
            # 0 : Collinear points, 1 : Clockwise points, 2 : Counterclockwise

            val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))

            if (val > 0):   # Clockwise orientation
                return 1
            elif (val < 0): # Counterclockwise orientation
                return 2
            else:           # Collinear orientation
                return 0

        def intersect(p1, q1, p2, q2):
            # Returns true if the line segment (p1,q1) and (p2,q2) intersect.

            # Find the 4 orientations required for general and special cases
            o1 = orientation(p1, q1, p2)
            o2 = orientation(p1, q1, q2)
            o3 = orientation(p2, q2, p1)
            o4 = orientation(p2, q2, q1)

            # General case
            if ((o1 != o2) and (o3 != o4)):
                return (True, [])

            collision_points = []

            # Colinear cases
            # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
            if ((o1 == 0) and on_segment(p1, p2, q1)):
                collision_points.append(p2)
            # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
            if ((o2 == 0) and on_segment(p1, q2, q1)):
                collision_points.append(q2)
            # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
            if ((o3 == 0) and on_segment(p2, p1, q2)):
                collision_points.append(p1)
            # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
            if ((o4 == 0) and on_segment(p2, q1, q2)):
                collision_points.append(q1)

            if collision_points:
                return (True, collision_points)
            else:
                return (False, [])

        def det(a, b):
            # Determinant function for finding non-colinear intersection point
            return (a[0] * b[1]) - (a[1] * b[0])

        # Initialize collisions list
        collisions = []

        # Loop through all the robot outline line segments, checking for collisions
        for bot_segment in self.outline_a_segments:
            # Check each line in the maze walls
            for square in wall_bounds:
                for line in square:

                    # Check whether segments intersect
                    intersections = intersect(*bot_segment, *line)

                    # If there are intersections, find the intersection points
                    if intersections[0]:

                        # If there are no colinear points
                        if not intersections[1]:
                            dx = (bot_segment[0][0] - bot_segment[1][0], line[0][0] - line[1][0])
                            dy = (bot_segment[0][1] - bot_segment[1][1], line[0][1] - line[1][1])
                            div = det(dx, dy)

                            if div != 0:
                                d = (det(*bot_segment), det(*line))
                                x = det(d, dx)/div
                                y = det(d, dy)/div
                                collisions.append((x,y))

                        # If there are colinear points
                        else:
                            for point in intersections[1]:
                                collisions.append(point)

        return collisions
