from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "Geospatial File Measurement API"
    assert data["version"] == "1.0.0"


def test_upload_unsupported_file():
    response = client.post(
        "/api/files/",
        files={
            "file": (
                "invalid.txt",
                b"hello",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Unsupported file type. "
        "Only KML and ZIP files are allowed."
    )


def test_get_nonexistent_file():
    response = client.get(
        "/api/files/"
        "00000000-0000-0000-0000-000000000000/"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"


def test_get_measurements_for_nonexistent_file():
    response = client.get(
        "/api/files/"
        "00000000-0000-0000-0000-000000000000/"
        "measurements/"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"


def test_upload_kml():
    kml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <Placemark>
        <name>Test Point</name>
        <Point>
            <coordinates>77.5946,12.9716</coordinates>
        </Point>
    </Placemark>

    <Placemark>
        <name>Test Line</name>
        <LineString>
            <coordinates>
                77.59,12.97
                77.60,12.98
            </coordinates>
        </LineString>
    </Placemark>

    <Placemark>
        <name>Test Polygon</name>
        <Polygon>
            <outerBoundaryIs>
                <LinearRing>
                    <coordinates>
                        77.59,12.97
                        77.60,12.97
                        77.60,12.98
                        77.59,12.98
                        77.59,12.97
                    </coordinates>
                </LinearRing>
            </outerBoundaryIs>
        </Polygon>
    </Placemark>
</Document>
</kml>
"""

    response = client.post(
        "/api/files/",
        files={
            "file": (
                "test_api.kml",
                BytesIO(kml_content),
                "application/vnd.google-earth.kml+xml"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "test_api.kml"
    assert data["file_type"] == "KML"
    assert data["status"] == "COMPLETED"
    assert data["feature_count"] == 3
    assert data["source_crs"] == "EPSG:4326"
    assert data["measurement_crs"] == "EPSG:32643"

    file_id = data["id"]

    measurements_response = client.get(
        f"/api/files/{file_id}/measurements/"
    )

    assert measurements_response.status_code == 200

    measurements = measurements_response.json()

    assert measurements["total_features"] == 3
    assert measurements["measured_features"] == 2
    assert measurements["not_required_features"] == 1
    assert measurements["unsupported_features"] == 0
    assert measurements["failed_features"] == 0

    # Area summary
    assert measurements["total_area"] is not None
    assert measurements["minimum_area"] is not None
    assert measurements["maximum_area"] is not None
    assert measurements["average_area"] is not None
    assert measurements["area_unit"] == "km2"

    # Length summary
    assert measurements["total_length"] is not None
    assert measurements["minimum_length"] is not None
    assert measurements["maximum_length"] is not None
    assert measurements["average_length"] is not None
    assert measurements["length_unit"] == "km"

    # Summary consistency checks
    assert measurements["minimum_area"] <= measurements["average_area"]
    assert measurements["average_area"] <= measurements["maximum_area"]

    assert measurements["minimum_length"] <= measurements["average_length"]
    assert measurements["average_length"] <= measurements["maximum_length"]


def test_upload_corrupted_zip():
    response = client.post(
        "/api/files/",
        files={
            "file": (
                "corrupted.zip",
                BytesIO(b"this is not a real zip"),
                "application/x-zip-compressed"
            )
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Invalid or corrupted ZIP file."
    )


def test_upload_shapefile_zip():
    zip_path = "sample_polygon.zip"

    with open(zip_path, "rb") as file:
        response = client.post(
            "/api/files/",
            files={
                "file": (
                    "sample_polygon.zip",
                    file,
                    "application/x-zip-compressed"
                )
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "sample_polygon.zip"
    assert data["file_type"] == "ZIP"
    assert data["status"] == "COMPLETED"
    assert data["feature_count"] == 1
    assert data["source_crs"] == "EPSG:4326"
    assert data["measurement_crs"] == "EPSG:32643"

    file_id = data["id"]

    measurements_response = client.get(
        f"/api/files/{file_id}/measurements/"
    )

    assert measurements_response.status_code == 200

    measurements = measurements_response.json()

    assert measurements["total_features"] == 1
    assert measurements["measured_features"] == 1
    assert measurements["not_required_features"] == 0
    assert measurements["unsupported_features"] == 0
    assert measurements["failed_features"] == 0

    # Area summary for the single polygon
    assert measurements["total_area"] is not None
    assert measurements["minimum_area"] is not None
    assert measurements["maximum_area"] is not None
    assert measurements["average_area"] is not None
    assert measurements["area_unit"] == "km2"

    assert (
        measurements["total_area"]
        == measurements["minimum_area"]
        == measurements["maximum_area"]
        == measurements["average_area"]
    )

    feature = measurements["measurements"][0]

    assert feature["geometry_type"] == "Polygon"
    assert feature["properties"]["Name"] == "Test Polygon"
    assert feature["measurement_type"] == "area"
    assert feature["measurement_unit"] == "km2"
    assert feature["measurement_status"] == "MEASURED"
    assert feature["measurement_value"] > 0

    assert (
        measurements["total_area"]
        == feature["measurement_value"]
    )


def test_uploads_with_same_filename_get_unique_storage_files():
    kml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <Placemark>
        <name>Test Point</name>
        <Point>
            <coordinates>77.5946,12.9716</coordinates>
        </Point>
    </Placemark>
</Document>
</kml>
"""

    first_response = client.post(
        "/api/files/",
        files={
            "file": (
                "duplicate.kml",
                BytesIO(kml_content),
                "application/vnd.google-earth.kml+xml"
            )
        }
    )

    second_response = client.post(
        "/api/files/",
        files={
            "file": (
                "duplicate.kml",
                BytesIO(kml_content),
                "application/vnd.google-earth.kml+xml"
            )
        }
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    first_data = first_response.json()
    second_data = second_response.json()

    # Original filename should remain unchanged
    assert first_data["filename"] == "duplicate.kml"
    assert second_data["filename"] == "duplicate.kml"

    # Each upload should create a different database record
    assert first_data["id"] != second_data["id"]