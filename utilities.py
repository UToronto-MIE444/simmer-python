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

import pygame
import config.config as CONFIG

def check_collision_walls(segments: list, walls: list):
    '''Checks for a collision between a set of line segments and a set of wall line segments.'''
    # Some code from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

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
    for segment in segments:
        # Check each line in the maze walls
        for square in walls:
            for line in square:

                # Check whether segments intersect
                intersections = intersect(*segment, *line)

                # If there are intersections, find the intersection points
                if intersections[0]:

                    # If there are no colinear points
                    if not intersections[1]:
                        dx = (segment[0][0] - segment[1][0], line[0][0] - line[1][0])
                        dy = (segment[0][1] - segment[1][1], line[0][1] - line[1][1])
                        div = det(dx, dy)

                        if div != 0:
                            d = (det(*segment), det(*line))
                            x = det(d, dx)/div
                            y = det(d, dy)/div
                            collisions.append((x,y))

                    # If there are colinear points
                    else:
                        for point in intersections[1]:
                            collisions.append(point)

    return collisions
