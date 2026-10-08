from app.geospatial.units import (
    convert_length,
    convert_area
)


def test_length_stays_in_meters():
    value, unit = convert_length(500)

    assert value == 500
    assert unit == "m"


def test_length_converts_to_kilometers():
    value, unit = convert_length(1500)

    assert value == 1.5
    assert unit == "km"


def test_area_stays_in_square_meters():
    value, unit = convert_area(5000)

    assert value == 5000
    assert unit == "m2"


def test_area_converts_to_hectares():
    value, unit = convert_area(50000)

    assert value == 5
    assert unit == "ha"


def test_area_converts_to_square_kilometers():
    value, unit = convert_area(2_000_000)

    assert value == 2
    assert unit == "km2"