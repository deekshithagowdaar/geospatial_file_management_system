from pathlib import Path

import geopandas as gpd


def read_kml(file_path: str | Path) -> gpd.GeoDataFrame:
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return gpd.read_file(
        file_path,
        driver="KML"
    )


def read_shapefile(
    file_path: str | Path
) -> gpd.GeoDataFrame:

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Shapefile not found: {file_path}"
        )

    return gpd.read_file(file_path)