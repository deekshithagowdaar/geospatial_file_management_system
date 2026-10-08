from shapely.geometry.base import BaseGeometry


SUPPORTED_GEOMETRIES = {
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
}


def validate_geometry(geometry: BaseGeometry | None) -> tuple[bool, str]:
    if geometry is None:
        return False, "NULL_GEOMETRY"

    if geometry.is_empty:
        return False, "EMPTY_GEOMETRY"

    if not geometry.is_valid:
        return False, "INVALID_GEOMETRY"

    if geometry.geom_type not in SUPPORTED_GEOMETRIES:
        return False, "UNSUPPORTED_GEOMETRY"

    return True, "VALID"