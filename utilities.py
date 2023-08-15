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

import math
import pygame
import config.config as CONFIG

def collision(segment1: list, segment2: list):
    '''
    Checks for a collision between two line segments in format [[x1, y1], [x2, y2]],
    returning intersect points in list or pygame.math.Vector2 format depending on
    the formats of segment1 and segment2.
    0 collisions - [Empty List]
    1 collision - [[x0, y0]]
    2 collisions - [[x0, y0], [x1, y1]]
    '''
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

    # Empty collision object
    collisions = []

    # Check whether segments intersect
    intersections = intersect(*segment1, *segment2)

    # If there are intersections, find the intersection points
    if intersections[0]:

        # If there are no colinear points
        if not intersections[1]:
            dx = (segment1[0][0] - segment1[1][0], segment2[0][0] - segment2[1][0])
            dy = (segment1[0][1] - segment1[1][1], segment2[0][1] - segment2[1][1])
            div = det(dx, dy)

            if div != 0:
                d = (det(*segment1), det(*segment2))
                x = det(d, dx)/div
                y = det(d, dy)/div
                collisions.append((x,y))

        # If there are colinear points
        else:
            for point in intersections[1]:
                collisions.append(point)

    return collisions

def closest(start: list, test_pts: list):
    '''Returns the closest point in the test_pts list to the point start.'''

    # If the list is empty, return the empty list
    if not test_pts:
        return test_pts

    # If there's only one point to test, it must be the closest. Return it.
    elif len(test_pts) == 1:
        return test_pts[0]

    # Otherwise calculate the closest point to the "start" point
    else:
        distance_minimum = math.inf
        for point in test_pts:
            vector = pygame.math.Vector2(point[0]-start[0], point[1]-start[0])
            distance = pygame.math.Vector2.magnitude(vector)
            if distance < distance_minimum:
                distance_minimum = distance

    return distance_minimum