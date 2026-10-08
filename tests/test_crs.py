import geopandas as gpd
import pytest
from shapely.geometry import Polygon

from app.geospatial.crs import get_measurement_crs


def test_missing_crs_raises_error():
    gdf = gpd.GeoDataFrame(
        geometry=[
            Polygon([
                (77.0, 13.0),
                (77.01, 13.0),
                (77.01, 13.01),
                (77.0, 13.01)
            ])
        ]
    )

    with pytest.raises(
        ValueError,
        match="Source CRS is missing."
    ):
        get_measurement_crs(gdf)


def test_geographic_crs_gets_projected_crs():
    gdf = gpd.GeoDataFrame(
        geometry=[
            Polygon([
                (77.0, 13.0),
                (77.01, 13.0),
                (77.01, 13.01),
                (77.0, 13.01)
            ])
        ],
        crs="EPSG:4326"
    )

    measurement_crs = get_measurement_crs(gdf)

    assert measurement_crs == "EPSG:32643"


def test_projected_crs_is_preserved():
    gdf = gpd.GeoDataFrame(
        geometry=[
            Polygon([
                (300000, 1400000),
                (300100, 1400000),
                (300100, 1400100),
                (300000, 1400100)
            ])
        ],
        crs="EPSG:32643"
    )

    measurement_crs = get_measurement_crs(gdf)

    assert measurement_crs == "EPSG:32643"


def test_only_empty_geometries_raise_error():
    gdf = gpd.GeoDataFrame(
        geometry=[Polygon()],
        crs="EPSG:4326"
    )

    with pytest.raises(
        ValueError,
        match="no valid geometries are available"
    ):
        get_measurement_crs(gdf)