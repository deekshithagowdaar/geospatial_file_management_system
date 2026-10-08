from shapely.geometry.base import BaseGeometry


def measure_geometry(
    geometry: BaseGeometry
) -> tuple[str | None, float | None, str | None, str]:

    geometry_type = geometry.geom_type

    if geometry_type in {"Point", "MultiPoint"}:
        return None, None, None, "NOT_REQUIRED"

    if geometry_type in {"LineString", "MultiLineString"}:
        return "length", float(geometry.length), "m", "MEASURED"

    if geometry_type in {"Polygon", "MultiPolygon"}:
        return "area", float(geometry.area), "m2", "MEASURED"

    return None, None, None, "UNSUPPORTED"