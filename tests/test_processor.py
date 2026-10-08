import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon

from app.geospatial.processor import process_geodata


def test_process_geodata_mixed_features():
    gdf = gpd.GeoDataFrame(
        {
            "Name": [
                "Test Point",
                "Test Line",
                "Test Polygon"
            ]
        },
        geometry=[
            Point(77.5946, 12.9716),
            LineString([
                (77.59, 12.97),
                (77.60, 12.98)
            ]),
            Polygon([
                (77.59, 12.97),
                (77.60, 12.97),
                (77.60, 12.98),
                (77.59, 12.98)
            ])
        ],
        crs="EPSG:4326"
    )

    result = process_geodata(gdf)

    assert result["feature_count"] == 3
    assert result["source_crs"] == "EPSG:4326"
    assert result["measurement_crs"] == "EPSG:32643"

    assert len(result["measurements"]) == 3

    assert result["measurements"][0]["geometry_type"] == "Point"
    assert result["measurements"][0]["measurement_status"] == "NOT_REQUIRED"

    assert result["measurements"][1]["geometry_type"] == "LineString"
    assert result["measurements"][1]["measurement_type"] == "length"
    assert result["measurements"][1]["measurement_status"] == "MEASURED"
    assert result["measurements"][1]["measurement_value"] > 0

    assert result["measurements"][2]["geometry_type"] == "Polygon"
    assert result["measurements"][2]["measurement_type"] == "area"
    assert result["measurements"][2]["measurement_status"] == "MEASURED"
    assert result["measurements"][2]["measurement_value"] > 0


def test_process_geodata_preserves_properties():
    gdf = gpd.GeoDataFrame(
        {
            "Name": ["Test Polygon"],
            "Category": ["Residential"]
        },
        geometry=[
            Polygon([
                (77.59, 12.97),
                (77.60, 12.97),
                (77.60, 12.98),
                (77.59, 12.98)
            ])
        ],
        crs="EPSG:4326"
    )

    result = process_geodata(gdf)

    properties = result["measurements"][0]["properties"]

    assert properties["Name"] == "Test Polygon"
    assert properties["Category"] == "Residential"


def test_process_geodata_handles_empty_geometry():
    valid_polygon = Polygon([
        (77.59, 12.97),
        (77.60, 12.97),
        (77.60, 12.98),
        (77.59, 12.98)
    ])

    empty_polygon = Polygon()

    gdf = gpd.GeoDataFrame(
        {
            "Name": [
                "Valid",
                "Empty"
            ]
        },
        geometry=[
            valid_polygon,
            empty_polygon
        ],
        crs="EPSG:4326"
    )

    result = process_geodata(gdf)

    assert len(result["measurements"]) == 2

    assert (
        result["measurements"][0]["measurement_status"]
        == "MEASURED"
    )

    assert (
        result["measurements"][1]["measurement_status"]
        == "FAILED"
    )

    assert (
        result["measurements"][1]["error"]
        == "EMPTY_GEOMETRY"
    )