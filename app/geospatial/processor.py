from pathlib import Path
from typing import Any

import pandas as pd
import geopandas as gpd

from app.geospatial.crs import get_measurement_crs
from app.geospatial.geometry import validate_geometry
from app.geospatial.measurement import measure_geometry
from app.geospatial.reader import read_kml, read_shapefile
from app.geospatial.units import convert_area, convert_length


def clean_property_value(value: Any) -> Any:
    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


def process_geodata(
    gdf: gpd.GeoDataFrame
) -> dict[str, Any]:

    measurement_crs = get_measurement_crs(gdf)

    projected_gdf = gdf.to_crs(measurement_crs)

    results = []

    for index, geometry in enumerate(projected_gdf.geometry):

        properties = {}

        for column in projected_gdf.columns:
            if column == "geometry":
                continue

            value = projected_gdf.iloc[index][column]
            value = clean_property_value(value)

            if value is not None:
                properties[column] = value

        is_valid, validation_status = validate_geometry(
            geometry
        )

        if not is_valid:
            results.append({
                "feature_index": index,
                "geometry_type": (
                    geometry.geom_type
                    if geometry is not None
                    else None
                ),
                "properties": properties,
                "measurement_type": None,
                "measurement_value": None,
                "measurement_unit": None,
                "measurement_status": "FAILED",
                "error": validation_status
            })
            continue

        measurement_type, value, unit, status = (
            measure_geometry(geometry)
        )

        if status == "NOT_REQUIRED":
            results.append({
                "feature_index": index,
                "geometry_type": geometry.geom_type,
                "properties": properties,
                "measurement_type": None,
                "measurement_value": None,
                "measurement_unit": None,
                "measurement_status": status
            })
            continue

        if measurement_type == "length":
            value, unit = convert_length(value)

        elif measurement_type == "area":
            value, unit = convert_area(value)

        results.append({
            "feature_index": index,
            "geometry_type": geometry.geom_type,
            "properties": properties,
            "measurement_type": measurement_type,
            "measurement_value": value,
            "measurement_unit": unit,
            "measurement_status": status
        })

    return {
        "source_crs": (
            gdf.crs.to_string()
            if gdf.crs
            else None
        ),
        "measurement_crs": measurement_crs,
        "feature_count": len(gdf),
        "measurements": results
    }


def process_kml(
    file_path: str | Path
) -> dict[str, Any]:

    gdf = read_kml(file_path)

    return process_geodata(gdf)


def process_shapefile(
    file_path: str | Path
) -> dict[str, Any]:

    gdf = read_shapefile(file_path)

    return process_geodata(gdf)