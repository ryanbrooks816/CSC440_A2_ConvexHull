import unittest
from collections import deque
from typing import List

from hypothesis import given
from hypothesis import strategies as st

from convex_hull import Point
from convex_hull import clockwise_sort
from convex_hull import compute_hull
from convex_hull import is_clockwise
from convex_hull import is_counter_clockwise
from convex_hull import y_intercept


class TestGivenFunctions(unittest.TestCase):
    """This class checks simple cases for the given functions."""
    def test_y_intercept(self):
        p1 = (0, 0)
        p2 = (20, 40)
        xs = [i for i in range(41)]
        for x in xs:
            y_int = y_intercept(p1, p2, x)
            self.assertAlmostEqual(2 * x, y_int, places=5)
        return

    def test_clockwise(self):
        p1 = (0, 0)
        p2 = (1, 0)
        p3 = (1, 1)

        self.assertTrue(is_clockwise(p1, p2, p3))
        self.assertFalse(is_clockwise(p1, p3, p2))
        return

    def test_counter_clockwise(self):
        p1 = (0, 0)
        p2 = (1, 0)
        p3 = (1, 1)

        self.assertTrue(is_counter_clockwise(p1, p3, p2))
        self.assertFalse(is_counter_clockwise(p1, p2, p3))
        return

    def test_clockwise_sort(self):
        p1 = (0, 0)
        p2 = (1, 0)
        p3 = (1, 1)
        p4 = (0, 1)
        points = [p2, p4, p1, p3]
        clockwise_sort(points)

        test_points = points + points[:2]
        for i in range(len(points)):
            a = test_points[i]
            b = test_points[i + 1]
            c = test_points[i + 2]
            self.assertTrue(is_clockwise(a, b, c))
        return


def is_convex_hull(hull: List[Point], points: List[Point]):
    vertices = hull + [hull[0]]
    prev_two = deque(maxlen=2)
    for vertex in vertices:
        prev_two.append(vertex)
        if len(prev_two) == 2:
            for point in points:
                assert not is_counter_clockwise(*prev_two, point)
    return True


class TestComputeHull(unittest.TestCase):
    @given(st.lists(  # generate a list
        st.tuples(  # of 2-tuples
            st.integers(min_value=0, max_value=100_000),  # of integers in the interval [0, 100_000]
            st.integers(min_value=0, max_value=100_000),
        ),
        min_size=3,  # minimum length of list
        max_size=100_000,  # maximum length of list
        unique=True,  # list will contain unique elements
    ))
    
    def test_compute_hull(self, points):
        points = list(points)
        clockwise_sort(points)

        hull = compute_hull(points)
        self.assertTrue(is_convex_hull(hull, points))
    
    def test_same_x_value_different_hulls(self):
        points = [(1, 1), (1, 4), (2, 2), (3, 3), (4, 1), (4, 4)]
        clockwise_sort(points)

        hull = compute_hull(points)
        self.assertTrue(is_convex_hull(hull, points))

    def test_same_x_value_different_hulls_case(self):
        points = [(1, 1), (1, 5), (2, 2), (3, 3), (4, 1), (4, 5)]
        clockwise_sort(points)

        hull = compute_hull(points)
        self.assertTrue(is_convex_hull(hull, points))

    def test_triangle_case(self):
        points = [(0, 0), (2, 2), (4, 0)]
        clockwise_sort(points)
        hull = compute_hull(points)
        self.assertCountEqual(hull, points)

    def test_collinear_points(self):
        points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
        clockwise_sort(points)
        hull = compute_hull(points)
        self.assertCountEqual(hull, [(0, 0), (4, 4)])

    def test_square_case(self):
        points = [(0, 0), (0, 2), (2, 2), (2, 0)]
        clockwise_sort(points)
        hull = compute_hull(points)
        self.assertCountEqual(hull, points)

    def test_duplicate_points(self):
        points = [(1, 1), (2, 2), (2, 2), (3, 3), (4, 4)]
        clockwise_sort(points)
        hull = compute_hull(points)
        self.assertNotIn((2, 2), hull[1:-1])  # Should only keep necessary points

    def test_single_point(self):
        points = [(3, 3)]
        hull = compute_hull(points)
        self.assertEqual(hull, [(3, 3)])

    def test_two_points(self):
        points = [(1, 1), (4, 4)]
        hull = compute_hull(points)
        self.assertCountEqual(hull, points)

    def test_star_shape(self):
        points = [(0, 0), (2, 3), (4, 0), (1, 1), (3, 1)]
        clockwise_sort(points)
        hull = compute_hull(points)
        self.assertCountEqual(hull, [(0, 0), (4, 0), (2, 3)])

    def test_cluster_with_outliers(self):
        points = [(1, 1), (2, 2), (3, 3), (1, 4), (4, 1), (0, 5), (5, 0)]
        clockwise_sort(points)
        hull = compute_hull(points)
        self.assertTrue(is_convex_hull(hull, points))

    def test_all_points_on_hull(self):
        points = [(0, 0), (1, 1), (2, 2), (2, 0), (0, 2)]
        clockwise_sort(points)
        hull = compute_hull(points)
        self.assertCountEqual(hull, points)

    def test_negative_coordinates(self):
        points = [(-3, -2), (-1, -5), (-4, -6), (-2, -1)]
        clockwise_sort(points)
        hull = compute_hull(points)
        self.assertTrue(is_convex_hull(hull, points))
        
if __name__ == '__main__':
    unittest.main()