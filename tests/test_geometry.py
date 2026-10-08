from shapely.geometry import (
    Point,
    LineString,
    Polygon,
    MultiPoint
)

from app.geospatial.geometry import validate_geometry


def test_valid_point():
    geometry = Point(77.5946, 12.9716)

    valid, status = validate_geometry(geometry)

    assert valid is True
    assert status == "VALID"


def test_valid_line_string():
    geometry = LineString([
        (77.0, 13.0),
        (77.01, 13.01)
    ])

    valid, status = validate_geometry(geometry)

    assert valid is True
    assert status == "VALID"


def test_valid_polygon():
    geometry = Polygon([
        (77.0, 13.0),
        (77.01, 13.0),
        (77.01, 13.01),
        (77.0, 13.01)
    ])

    valid, status = validate_geometry(geometry)

    assert valid is True
    assert status == "VALID"


def test_valid_multi_point():
    geometry = MultiPoint([
        (77.0, 13.0),
        (77.01, 13.01)
    ])

    valid, status = validate_geometry(geometry)

    assert valid is True
    assert status == "VALID"


def test_null_geometry():
    valid, status = validate_geometry(None)

    assert valid is False
    assert status == "NULL_GEOMETRY"


def test_empty_geometry():
    geometry = Polygon()

    valid, status = validate_geometry(geometry)

    assert valid is False
    assert status == "EMPTY_GEOMETRY"


def test_invalid_polygon():
    geometry = Polygon([
        (0, 0),
        (1, 1),
        (1, 0),
        (0, 1),
        (0, 0)
    ])

    valid, status = validate_geometry(geometry)

    assert valid is False
    assert status == "INVALID_GEOMETRY"