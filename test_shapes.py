import pytest

from geometry import shapes


def test_orientation_left():
    assert shapes.orientation([0, 0], [1, 0], [0, 1]) == 1


def test_orientation_right():
    assert shapes.orientation([0, 0], [1, 0], [0, -1]) == -1


def test_collinear():
    assert shapes.collinear([0, 0], [1, 1], [2, 2]) is True


def test_point_line_distance():
    assert shapes.point_line_distance([0, 2], [0, 0], [1, 0]) == 2.0


def test_segment_intersection_cross():
    point = shapes.segment_intersection([-1, 0], [1, 0], [0, -1], [0, 1])
    assert point == pytest.approx([0.0, 0.0])


def test_segment_intersection_none():
    assert shapes.segment_intersection([0, 0], [1, 0], [0, 1], [1, 1]) is None


def test_polygon_area_unit_square():
    assert shapes.polygon_area([[0, 0], [1, 0], [1, 1], [0, 1]]) == 1.0


def test_point_in_polygon():
    square = [[0, 0], [4, 0], [4, 4], [0, 4]]
    assert shapes.point_in_polygon([2, 2], square) is True
    assert shapes.point_in_polygon([5, 5], square) is False


def test_is_convex_square():
    assert shapes.is_convex([[0, 0], [1, 0], [1, 1], [0, 1]]) is True