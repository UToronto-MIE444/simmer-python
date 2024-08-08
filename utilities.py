'''
A collection of utility functions for SimMeR.
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
import random
import pygame
import config as CONFIG
from collections import Counter

def add_error(value: float, pct_error: float, bounds: list = [],sigma=2):
    '''
    ADD_ERROR Adds normally distributed percent error to a measurement
    As an input, this function takes a measurement value and an error
    percentage (from 0 to 1). It uses randn to calculate a normally
    distributed error and add it to the value and output it.

    bounds is an optional two-value vector that can be added to specify
    limits to the returned values. For example, if bounds is [0 1], values
    will be limited to those within the given values
    '''

    def clamp(number, bounds):
        return max(min(bounds[1], number), bounds[0])

    # Calculate the error value
    error_value = random.gauss(0,sigma) * pct_error * value
    # Add to the original value
    value_noisy = value + error_value
    # Clamp it to the specified bounds
    if bounds:
        return clamp(value_noisy, bounds)
    else:
        return value_noisy


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
    '''
    Returns the closest point in the test_pts list to the point start, and
    the Euclidean distance between them.
    '''

    # If the list is empty, return the empty list and a nan for length
    if not test_pts:
        return test_pts, math.nan

    # Otherwise calculate the closest point to the "start" point
    else:
        distance_minimum = math.inf
        closest_pt = []
        for test_pt in test_pts:
            vector = pygame.math.Vector2(test_pt[0]-start[0], test_pt[1]-start[1])
            distance = pygame.math.Vector2.magnitude(vector)
            if distance < distance_minimum:
                distance_minimum = distance
                closest_pt = test_pt

    return closest_pt, distance_minimum


def simulate_sensors(environment, sensors):
    '''Simulate a list of sensors'''

    ROBOT = environment.get("ROBOT", None)
    for d_id in sensors:
        if d_id in ROBOT.sensors:
            ROBOT.sensors[d_id].simulate(0, environment)


def angle(segment1:list, segment2:list):

    theta1 = math.degrees(math.atan2(segment1[0][1]-segment1[1][1],segment1[0][0]-segment1[1][0]))
    theta2 = math.degrees(math.atan2(segment2[0][1]-segment2[1][1],segment2[0][0]-segment2[1][0]))

    diff = abs(theta1 - theta2)

    # while diff>=360:
    #     diff-=360

    if diff>270:
        return 360-diff
    if diff>180:
        return diff - 180
    if diff>90:
        return 180 - diff


def closest_fast(start: list, test_pts: list):
    '''
    Returns the closest point in the test_pts list to the point start, and
    the SQUARED Euclidean distance between them.
    '''

    # If the list is empty, return the empty list and a nan for length
    if not test_pts:
        return test_pts, math.nan

    # Otherwise calculate the closest point to the "start" point
    else:
        distSq_minimum = math.inf
        closest_pt = []
        for test_pt in test_pts:
            # calculates squared distance between start and test_pt (to avoid sqrt calculation)
            distSq = (test_pt[0] - start[0]) ** 2 + (test_pt[1] - start[1]) ** 2

            # minimum squared distance corresponds to minimum distance
            if distSq < distSq_minimum:
                distSq_minimum = distSq
                closest_pt = test_pt

    return closest_pt, distSq_minimum


def is_vertical(line_segment):
    return line_segment[0][0] == line_segment[1][0]


def slopeIntercept(segment):
    '''
    Returns the slope and the intercept of a line segment
    '''

    # Check if two line segments are parallel, handling vertical lines
    dx = segment[1][0] - segment[0][0]

    if dx == 0:
        # Both segments are vertical, consider them parallel
        slope = math.inf

    else:
        # Check the slope for non-vertical segments
        slope = (segment[1][1] - segment[0][1]) / dx

    intercept = segment[0][1] - slope * segment[0][0]

    return slope, intercept


def merge_sloped_line_segments(line_segments):
    '''
    takes a list of line 2d segments (list of list of lists)
    returns reduced list where colinear intersecting lines
    are joined into a single line.

    works for lines that are NOT vertical
    '''

    if not line_segments:
        return []

    for i in range(len(line_segments)):
        # sorts on x values, ensuring left point is fist
        line_segments[i].sort()

    # sorts on first x value of each line, if equal,
    # uses first y value >> second x value >> second y value
    line_segments.sort()

    non_duplicate_segments = remove_duplicates(line_segments)

    merged_segments = []
    merged_indices = []

    # [[[0, 0], [1, 1]], [[0.9, 0.9], [4, 4]], [[2, 2], [4, 4]], [[5, 5], [7, 7]]]
    for i, segment1 in enumerate(non_duplicate_segments):
        if i in merged_indices:
            # this line segment has already been merged with one before it. ignore.
            continue

        current_segment = segment1.copy()

        for j, segment2 in enumerate(non_duplicate_segments[i + 1 :]):
            # right most point of seg1 is left of leftmost point of seg2. intersection impossible
            if segment2[0][0] > current_segment[1][0]:
                break  # breaks out of j loop

            if slopeIntercept(segment1) == slopeIntercept(segment2):
                current_segment = [current_segment[0], max(segment1[1], segment2[1])]
                merged_indices.append(i + j + 1)  # index of segment2 in line_segments

        merged_segments.append(current_segment)

    return merged_segments


def merge_vertical_line_segments(line_segments):
    '''
    takes a list of line 2d segments (list of list of lists)
    returns reduced list where colinear intersecting lines
    are joined into a single line.

    works for lines that are ONLY vertical
    '''

    if not line_segments:
        return []

    for ls in line_segments:
        if not is_vertical(ls):
            b = (
                repr(ls)
                + " is not vertical. input_list[0][0] should equal input_list[1][0]"
            )
            raise ValueError(b)

        # sort on y values, i.e. make sure all lines start point is the bottom
        ls.sort(key=lambda pt: pt[1])
    # sort on x values, i.e. order line segments from left to right
    line_segments.sort()

    non_duplicate_segments = remove_duplicates(line_segments)

    merged_segments = []
    current_segment = non_duplicate_segments[0]
    for next_segment in non_duplicate_segments[1:]:
        # if colinear and overlapping
        if (
            current_segment[0][0] == next_segment[0][0]
            and current_segment[1][1] >= next_segment[0][1]
        ):
            # Overlapping and parallel, merge the segments
            current_segment[1] = [
                current_segment[0][0],
                max(current_segment[1][1], next_segment[1][1]),
            ]
        else:
            # Non-overlapping or not parallel, add the current segment to the result
            merged_segments.append(current_segment)
            current_segment = next_segment

            # Add the last segment
    merged_segments.append(current_segment)
    return merged_segments


def optimize_walls(line_segments):
    '''
    takes a list of walls (line_segments)
    deletes shared walls of neighboring blocks (both instances)
    merges collinear intersecting/overlapping walls
    returns reduced list of walls
    '''
    if not line_segments:
        return []

    for i in range(len(line_segments)):
        # sorts on x values, ensuring left point is fist
        line_segments[i].sort()

    # sorts on first x value of each line, if equal,
    # uses first y value >> second x value >> second y value
    line_segments.sort()

    # Flatten the list of lists of lists to a list of tuples
    ls_tuples = [tuple([tuple(pt) for pt in ls]) for ls in line_segments]

    counts=Counter(ls_tuples)

    fewer_segment_tuples = [element for element, count in counts.items() if count == 1]

    # Convert back to a list of lists of lists
    fewer_segments = [[list(inner_tuple) for inner_tuple in outer_tuple] for outer_tuple in fewer_segment_tuples]
    vert = []
    non_vert = []

    for ls in fewer_segments:
        if is_vertical(ls):
            vert.append(ls)
        else:
            non_vert.append(ls)

    return merge_sloped_line_segments(non_vert) + merge_vertical_line_segments(vert)


def remove_duplicates(sorted_list:list)->list:
    '''
    returns a list of elements that ONLY show up once in the input list
    '''
    unique_list = []

    i = 0
    while i < len(sorted_list):
        current = sorted_list[i]

        # Skip all occurrences of the current element
        while i < len(sorted_list) and sorted_list[i] == current:
            i += 1

        # If there was only one occurrence, add it to the result
        if i == sorted_list.index(current) + 1:
            unique_list.append(current)

    return unique_list


def in_block(vec):
    '''determins whether a vector is inside a wall block or not'''

    x_idx = int(vec.x//CONFIG.wall_segment_length)
    y_idx = int(vec.y//CONFIG.wall_segment_length)

    return CONFIG.walls[y_idx][x_idx]==0


def check_collision_fast(s1: list, s2: list) -> bool:
    '''
    returns whether or not two line segments are intersecting, without calculating intersection points
    '''

    def onSegment(p, q, r):
        if (
            (q[0] <= max(p[0], r[0]))
            and (q[0] >= min(p[0], r[0]))
            and (q[1] <= max(p[1], r[1]))
            and (q[1] >= min(p[1], r[1]))
        ):
            return True
        return False

    def orientation(p, q, r):
        # to find the orientation of an ordered triplet (p,q,r)
        # function returns the following values:
        # 0 : Collinear points
        # 1 : Clockwise points
        # 2 : Counterclockwise

        # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
        # for details of below formula.

        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val > 0:
            # Clockwise orientation
            return 1
        elif val < 0:
            # Counterclockwise orientation
            return 2
        else:
            # Collinear orientation
            return 0

    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(s1[0], s1[1], s2[0])
    o2 = orientation(s1[0], s1[1], s2[1])
    o3 = orientation(s2[0], s2[1], s1[0])
    o4 = orientation(s2[0], s2[1], s1[1])

    # General case
    if (o1 != o2) and (o3 != o4):
        return True

    # Special Cases

    # s1[0] , s1[1] and s2[0] are collinear and s2[0] lies on segment s1[0]s1[1]
    if (o1 == 0) and onSegment(s1[0], s2[0], s1[1]):
        return True

    # s1[0] , s1[1] and s2[1] are collinear and s2[1] lies on segment s1[0]s1[1]
    if (o2 == 0) and onSegment(s1[0], s2[1], s1[1]):
        return True

    # s2[0] , s2[1] and s1[0] are collinear and s1[0] lies on segment s2[0]s2[1]
    if (o3 == 0) and onSegment(s2[0], s1[0], s2[1]):
        return True

    # s2[0] , s2[1] and s1[1] are collinear and s1[1] lies on segment s2[0]s2[1]
    if (o4 == 0) and onSegment(s2[0], s1[1], s2[1]):
        return True

    # If none of the cases
    return False
