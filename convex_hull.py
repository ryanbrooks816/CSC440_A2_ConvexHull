import math
import sys
from typing import List
from typing import Tuple

EPSILON = sys.float_info.epsilon
Point = Tuple[int, int]


def y_intercept(p1: Point, p2: Point, x: int) -> float:
    """
    Given two points, p1 and p2, an x coordinate from a vertical line,
    compute and return the the y-intercept of the line segment p1->p2
    with the vertical line passing through x.
    """
    x1, y1 = p1
    x2, y2 = p2
    slope = (y2 - y1) / (x2 - x1)
    return y1 + (x - x1) * slope


def triangle_area(a: Point, b: Point, c: Point) -> float:
    """
    Given three points a,b,c,
    computes and returns the area defined by the triangle a,b,c.
    Note that this area will be negative if a,b,c represents a clockwise sequence,
    positive if it is counter-clockwise,
    and zero if the points are collinear.
    """
    ax, ay = a
    bx, by = b
    cx, cy = c
    return ((cx - bx) * (by - ay) - (bx - ax) * (cy - by)) / 2


def is_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) < -EPSILON


def is_counter_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a counter-clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) > EPSILON


def collinear(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c are collinear
    (subject to floating-point precision)
    """
    return abs(triangle_area(a, b, c)) <= EPSILON


def clockwise_sort(points: List[Point]):
    """
    Given a list of points, sorts those points in clockwise order about their centroid.
    Note: this function modifies its argument.
    """
    # get mean x coord, mean y coord
    x_mean = sum(p[0] for p in points) / len(points)
    y_mean = sum(p[1] for p in points) / len(points)

    def angle(point: Point):
        return (math.atan2(point[1] - y_mean, point[0] - x_mean) + 2 * math.pi) % (2 * math.pi)

    points.sort(key=angle)
    return


def compute_hull(points: List[Point]) -> List[Point]:
    """
    Given a list of points, recursively computes the convex hull around those points
    by dividing the points into two halves, computing the hulls of the two halves, and
    merging the hulls.
    
    Invariant: Through each step in the process, the outputted list of Points will only
    contain points that cause it to be a valid convex hull.
    
    Initialization:
        - At the start, the list of points on the hull is empty, so it does not contain
          any points that would invalidate the convex hull, so the invariant holds.
        - The points are sorted by x and y coordinates, giving a total of 
          O(nlogn) operations.
    Maintenance:
        - The points are recursively divided into two halves, left and right, and contains
          all the points that would be in or on the convex hull.
        - This happens until the base case of <= 6 points in a hull is reached.
          From there, the base case is called with the points and returns a valid convex 
          hull, so the invariant still holds.
        - The hulls from both halves are merged by finding the upper and lower tangents of 
          the two hulls, connecting them, and removing old inner points. The only place
          where this function is called is with the two hulls found via the base case, and
          the merged list of points returned contains only the points that make up the valid
          convex hull, so the invariant still holds.
    Termination:
        - All recursive calls have been made and all hulls have been merged. The final
          list of points returned contains all of the points that make up the complete
          convex hull of all the sub-hulls, so the invariant holds.
        - The final set of points is sorted in clockwise order.
    """
    # No further work needed, returns points in clockwise order
    if len(points) <= 1:
        return points
    if len(points) <= 3:
        clockwise_sort(points)
        return points
    
    # Sort the points by x-coordinate
    points.sort()

    def divide_hull(points: List[Point]) -> List[Point]:
        if len(points) <= 6:
            return base_case_hull(points)
        
        # Divide the points into two halves
        mid = len(points) // 2
        left_points = points[:mid]
        right_points = points[mid:]

        # Recursively compute the hulls of the two halves
        left_hull = divide_hull(left_points)
        right_hull = divide_hull(right_points)
        
        # Merge the two hulls
        return merge_hulls(left_hull, right_hull)

    # Sort the complete hull in clockwise order
    complete_hull = divide_hull(points)
    
    clockwise_sort(complete_hull)
    return complete_hull


def base_case_hull(points: List[Point]) -> List[Point]:
    """
    Base case of the recursive algorithm. Given a sorted list of points that is 
    <= 6 and > 3, compute the convex hull around  those points using the Monotone Chain
    algorithm to construct lower and upper hulls.
    
    Invariant: The lower and upper hulls are valid convex hulls. The following
    substantiates this claim of the main algorithm.
    
    Initialization:
        - The lower and upper hulls are empty. The lower hull represents the bottom half
          of the convex hull from the leftmost point to the rightmost point. The upper hull
          represents the top half of the convex hull from the rightmost point to the leftmost
          point.
    Maintenance:
        - Each point is processed exactly once.
        - The lower and upper hulls are always valid convex hulls.
        - The lower hull moves from left to right, avoiding turns to the right and 
          the upper hull moves from right to left, avoiding turns to the left. Doing
          so maintains the convex property of the hulls.
        - In other words, they are only added if they are counter-clockwise with 
          respect to the last two points in the hull, which is calculated using the 
          triangle area of the last two points and the current point `p`.
        - Each point can be pushed and popped from the hulls at most once, giving
          a total of O(n) operations.
    Termination:
        - All points have been processed.
        - The lower and upper hulls form the complete convex hull without duplicates
          sorted in counter-clockwise order.
    """
    # Build the lower hull 
    lower = []
    for p in points:
        while len(lower) >= 2 and not is_counter_clockwise(lower[-2], lower[-1], p):
            lower.pop()
        lower.append(p)

    # Build the upper hull
    upper = []
    for i in range(len(points) - 1, -1, -1):
        p = points[i]
        while len(upper) >= 2 and not is_counter_clockwise(upper[-2], upper[-1], p):
            upper.pop()
        upper.append(p)

    # Concatenate lower and upper hull to make the full hull
    # Remove the last point of each half to avoid duplication
    return lower[:-1] + upper[:-1]


def merge_hulls(left_hull: List[Point], right_hull: List[Point]) -> List[Point]:
    """
    Given two convex hulls, left_hull and right_hull, merge them into a single convex hull
    by finding the upper and lower tangents and removing points that fall within the
    merged hulls.
    
    Invariant: The merged hull is a valid convex hull. The following substantiates this 
    claim of the main algorithm.
    
    Initialization:
        - The left and right hulls start as valid convex hulls as was aleady shown in 
          the main algorithm and divide function.
        - The upper and lower tangents have been computed and are points found on the 
          hulls such that the upper tangent connects exactly one point from the left hull
          to exactly one point from the right hull given no other points lie above the line,
          and the opposite for the lower tangent, where no points lie below the line.
    Maintenance:
        - We iterate through the points in the left hull from the upper tangent to the lower
          tangent, and then through the points in the right hull from the lower tangent to the
          upper tangent, moving counterclockwise.
        - The merged hull is a valid convex hull as the points are added in a way that maintains
          the convexity of the hull since we are only traversing the outer borders of the hulls,
          as such the invariant holds.
    Termination:
        - The result is a merged hull that is a valid convex hull.
    """
    # Find upper and lower tangents
    (upper_tangent, lower_tangent) = find_tangents(left_hull, right_hull) 
    
    upper_left, upper_right = upper_tangent
    lower_left, lower_right = lower_tangent

    # Collect points from the left hull (counterclockwise from upper to lower tangent)
    merged_hull = []
    i = upper_left
    while i != lower_left:
        merged_hull.append(left_hull[i])
        i = (i + 1) % len(left_hull)  # move counterclockwise
    merged_hull.append(left_hull[lower_left])  # add last point in left hull

    # Collect points from the right hull (counterclockwise from lower to upper tangent)
    i = lower_right
    while i != upper_right:
        merged_hull.append(right_hull[i])
        i = (i + 1) % len(right_hull)  # move counterclockwise
    merged_hull.append(right_hull[upper_right])  # add last point in right hull

    return merged_hull


def find_tangents(left_hull: List[Point], right_hull: List[Point]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Finds the upper and lower tangent points between two convex hulls and returns the
    indices of the points in the hulls (upper_left, upper_right) and (lower_left, lower_right).
    """
    def next_index(hull, index):
        return (index + 1) % len(hull)

    def prev_index(hull, index):
        return (index - 1) % len(hull)

    def find_tangent(left_hull, right_hull, left_point_idx, right_point_idx, traversal_f, next_f, prev_f):
        # Find the tangent by moving along the hulls until no more points can be added
        while True:
            moved = False
            # Move along the left hull until the next point is not counterclockwise
            while traversal_f(left_hull[left_point_idx], right_hull[right_point_idx], left_hull[next_f(left_hull, left_point_idx)]):
                left_point_idx = next_f(left_hull, left_point_idx)
                moved = True
            # Move along the right hull in the opposite direction
            while traversal_f(left_hull[left_point_idx], right_hull[right_point_idx], right_hull[prev_f(right_hull, right_point_idx)]):
                right_point_idx = prev_f(right_hull, right_point_idx)
                moved = True
            # If no points were added, the tangent is found
            if not moved:
                break
        return left_point_idx, right_point_idx
    
    # Start with the rightmost point in the left hull and the leftmost point in the right hull
    rightmost_left = left_hull.index(max(left_hull))
    leftmost_right = right_hull.index(min(right_hull))
    
    # Find the upper and lower tangent
    upper_tangent = find_tangent(left_hull, right_hull, rightmost_left, leftmost_right, is_counter_clockwise, next_index, prev_index)
    lower_tangent = find_tangent(left_hull, right_hull, rightmost_left, leftmost_right, is_clockwise, prev_index, next_index)

    return upper_tangent, lower_tangent