import geopandas as gpd


def get_measurement_crs(gdf: gpd.GeoDataFrame) -> str:
    if gdf.crs is None:
        raise ValueError("Source CRS is missing.")

    if not gdf.crs.is_geographic:
        return gdf.crs.to_string()

    valid_indices = []

    for index, geometry in gdf.geometry.items():
        if geometry is not None and not geometry.is_empty:
            valid_indices.append(index)

    if not valid_indices:
        raise ValueError(
            "Unable to determine measurement CRS: "
            "no valid geometries are available."
        )

    valid_gdf = gdf.loc[valid_indices]

    return valid_gdf.estimate_utm_crs().to_string()