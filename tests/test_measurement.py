from shapely.geometry import (
    Point,
    LineString,
    Polygon,
    MultiPoint,
    MultiLineString,
    MultiPolygon
)

from app.geospatial.measurement import measure_geometry


def test_point_does_not_require_measurement():
    geometry = Point(77.5946, 12.9716)

    measurement_type, value, unit, status = measure_geometry(
        geometry
    )

    assert measurement_type is None
    assert value is None
    assert unit is None
    assert status == "NOT_REQUIRED"


def test_multipoint_does_not_require_measurement():
    geometry = MultiPoint([
        (77.5946, 12.9716),
        (77.60, 12.98)
    ])

    measurement_type, value, unit, status = measure_geometry(
        geometry
    )

    assert measurement_type is None
    assert value is None
    assert unit is None
    assert status == "NOT_REQUIRED"


def test_line_string_measurement():
    geometry = LineString([
        (0, 0),
        (100, 0)
    ])

    measurement_type, value, unit, status = measure_geometry(
        geometry
    )

    assert measurement_type == "length"
    assert value == 100.0
    assert unit == "m"
    assert status == "MEASURED"


def test_multi_line_string_measurement():
    geometry = MultiLineString([
        [(0, 0), (100, 0)],
        [(0, 0), (0, 50)]
    ])

    measurement_type, value, unit, status = measure_geometry(
        geometry
    )

    assert measurement_type == "length"
    assert value == 150.0
    assert unit == "m"
    assert status == "MEASURED"


def test_polygon_measurement():
    geometry = Polygon([
        (0, 0),
        (10, 0),
        (10, 10),
        (0, 10)
    ])

    measurement_type, value, unit, status = measure_geometry(
        geometry
    )

    assert measurement_type == "area"
    assert value == 100.0
    assert unit == "m2"
    assert status == "MEASURED"


def test_multipolygon_measurement():
    geometry = MultiPolygon([
        Polygon([
            (0, 0),
            (10, 0),
            (10, 10),
            (0, 10)
        ]),
        Polygon([
            (20, 0),
            (30, 0),
            (30, 10),
            (20, 10)
        ])
    ])

    measurement_type, value, unit, status = measure_geometry(
        geometry
    )

    assert measurement_type == "area"
    assert value == 200.0
    assert unit == "m2"
    assert status == "MEASURED"