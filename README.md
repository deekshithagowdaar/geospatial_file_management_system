### README

# Geospatial File Measurement API

A FastAPI-based backend for uploading KML files and Shapefile ZIP archives, extracting geospatial features and attributes, handling coordinate reference systems correctly, and calculating geometry measurements such as area and length.

---

## Features

- Upload KML files
- Upload Shapefile ZIP archives
- Validate uploaded file types and file sizes
- Safely extract ZIP files
- Validate required Shapefile components
- Detect corrupted or malformed files
- Extract:
  - Feature index
  - Geometry type
  - Feature properties/attributes
  - Source CRS
- Validate geometries
- Handle:
  - Point
  - MultiPoint
  - LineString
  - MultiLineString
  - Polygon
  - MultiPolygon
- Calculate:
  - Polygon/MultiPolygon area
  - LineString/MultiLineString length
- Do not calculate measurements for Point/MultiPoint features
- Automatically select a suitable projected CRS for geographic data
- Convert measurements into readable units
- Store file metadata and measurements in SQLite
- Provide measurement summaries
- Structured API error handling
- Application logging
- Automated pytest test suite
- Swagger/OpenAPI documentation
- Docker containerization

---

## Tech Stack

- Python
- FastAPI
- GeoPandas
- Shapely
- PyProj
- Fiona
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- Uvicorn
- Docker

---

## Architecture

```text
Client
  |
  | POST KML / Shapefile ZIP
  v
FastAPI
  |
  +-- File Validation
  |
  +-- File Storage
  |
  +-- Geospatial Processing
  |      |
  |      +-- Read KML / Shapefile
  |      +-- Validate Geometry
  |      +-- Handle CRS
  |      +-- Calculate Area / Length
  |      +-- Convert Units
  |
  +-- Database
         |
         +-- files
         |
         +-- feature_measurements
```

---

## Project Structure

```text
geospatial-measurement-api/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   │
│   ├── api/
│   │   └── routes/
│   │       └── files.py
│   │
│   ├── models/
│   │   ├── file.py
│   │   └── feature_measurement.py
│   │
│   ├── schemas/
│   │   ├── file.py
│   │   ├── feature_measurement.py
│   │   └── measurement.py
│   │
│   ├── services/
│   │   ├── file_storage.py
│   │   ├── file_validator.py
│   │   └── geospatial_service.py
│   │
│   ├── geospatial/
│   │   ├── reader.py
│   │   ├── geometry.py
│   │   ├── crs.py
│   │   ├── measurement.py
│   │   ├── units.py
│   │   ├── processor.py
│   │   └── shapefile.py
│   │
│   └── db/
│       ├── database.py
│       └── init_db.py
│
├── tests/
│   ├── test_geometry.py
│   ├── test_measurement.py
│   ├── test_units.py
│   ├── test_crs.py
│   ├── test_processor.py
│   └── test_api.py
│
├── uploads/
│   └── .gitkeep
│
├── Dockerfile
├── .dockerignore
├── .env.example
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Requirements

- Python 3.11+
- pip
- Windows, Linux, or macOS
- Docker Desktop (for containerized execution)

---

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/deekshithagowdaar/geospatial_file_management_system.git
cd geospatial_file_management_system
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root:

```env
APP_NAME=Geospatial File Measurement API
APP_VERSION=1.0.0
DATABASE_URL=sqlite:///./geospatial.db
MAX_UPLOAD_SIZE_MB=50
```

The maximum upload size is configurable using:

```env
MAX_UPLOAD_SIZE_MB=50
```

---

## Run the Application

Start the FastAPI server:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## Docker

### Build the Docker image

```powershell
docker build -t geospatial-measurement-api .
```

### Run the container

```powershell
docker run --name geospatial-api --env-file .env -p 8000:8000 geospatial-measurement-api
```

The API will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

The application automatically initializes the SQLite database when the container starts.

---

## API Documentation

FastAPI automatically provides Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

---

## API Endpoints

### Health Check

```text
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "Geospatial File Measurement API",
  "version": "1.0.0"
}
```

---

### Upload File

```text
POST /api/files/
```

Supported files:

- `.kml`
- `.zip` containing a Shapefile

Example using curl:

```powershell
curl -X POST "http://127.0.0.1:8000/api/files/" `
  -H "accept: application/json" `
  -H "Content-Type: multipart/form-data" `
  -F "file=@sample.kml"
```

Example response:

```json
{
  "id": "6f118df4-347d-4336-8fb1-c2428b70b6c6",
  "filename": "sample.kml",
  "file_type": "KML",
  "status": "COMPLETED",
  "feature_count": 3,
  "source_crs": "EPSG:4326",
  "measurement_crs": "EPSG:32643",
  "created_at": "2026-10-08T06:07:47.328847"
}
```

---

### Get File Metadata

```text
GET /api/files/{file_id}/
```

Returns information about the uploaded file and its processing status.

---

### Get Measurements

```text
GET /api/files/{file_id}/measurements/
```

Returns:

- Feature counts
- Area summary
- Length summary
- Individual feature measurements
- Feature properties
- Measurement status

Example:

```json
{
  "file_id": "6f118df4-347d-4336-8fb1-c2428b70b6c6",
  "total_features": 3,
  "measured_features": 2,
  "not_required_features": 1,
  "unsupported_features": 0,
  "failed_features": 0,
  "total_area": 1.2016847167952391,
  "minimum_area": 1.2016847167952391,
  "maximum_area": 1.2016847167952391,
  "average_area": 1.2016847167952391,
  "area_unit": "km2",
  "total_length": 1.5504276666371866,
  "minimum_length": 1.5504276666371866,
  "maximum_length": 1.5504276666371866,
  "average_length": 1.5504276666371866,
  "length_unit": "km",
  "measurements": [
    {
      "id": 1,
      "file_id": "6f118df4-347d-4336-8fb1-c2428b70b6c6",
      "feature_index": 0,
      "geometry_type": "Point",
      "properties": {
        "Name": "Test Point",
        "tessellate": -1,
        "extrude": 0,
        "visibility": -1
      },
      "measurement_type": null,
      "measurement_value": null,
      "measurement_unit": null,
      "measurement_status": "NOT_REQUIRED"
    },
    {
      "id": 2,
      "file_id": "6f118df4-347d-4336-8fb1-c2428b70b6c6",
      "feature_index": 1,
      "geometry_type": "LineString",
      "properties": {
        "Name": "Test Line",
        "tessellate": -1,
        "extrude": 0,
        "visibility": -1
      },
      "measurement_type": "length",
      "measurement_value": 1.5504276666371866,
      "measurement_unit": "km",
      "measurement_status": "MEASURED"
    },
    {
      "id": 3,
      "file_id": "6f118df4-347d-4336-8fb1-c2428b70b6c6",
      "feature_index": 2,
      "geometry_type": "Polygon",
      "properties": {
        "Name": "Test Polygon",
        "tessellate": -1,
        "extrude": 0,
        "visibility": -1
      },
      "measurement_type": "area",
      "measurement_value": 1.2016847167952391,
      "measurement_unit": "km2",
      "measurement_status": "MEASURED"
    }
  ]
}
```

---

## Measurement Rules

### Point

No area or length measurement is required.

Status:

```text
NOT_REQUIRED
```

### MultiPoint

No area or length measurement is required.

Status:

```text
NOT_REQUIRED
```

### LineString

Length is calculated.

```text
measurement_type = length
```

### MultiLineString

Total length of all line components is calculated.

```text
measurement_type = length
```

### Polygon

Area is calculated.

```text
measurement_type = area
```

### MultiPolygon

Combined area of all polygon components is calculated.

```text
measurement_type = area
```

---

## CRS Handling

Correct CRS handling is important because geographic coordinates such as latitude and longitude are expressed in degrees and should not be directly used for metric area or length calculations.

For example:

```text
EPSG:4326
```

uses latitude/longitude coordinates.

The application therefore determines a suitable projected CRS before calculating measurements.

Example:

```text
Source CRS:
EPSG:4326

Measurement CRS:
EPSG:32643
```

For projected source data, the existing projected CRS is preserved.

If the source CRS is missing, the application does not silently guess it.

---

## Geometry Validation

The application checks geometries for:

- Null geometry
- Empty geometry
- Invalid geometry
- Unsupported geometry types

Invalid features are recorded with an appropriate measurement status instead of silently producing incorrect measurements.

---

## Unit Conversion

### Length

The application uses:

```text
m
km
```

Conversion example:

```text
1500 m → 1.5 km
```

### Area

The application uses:

```text
m2
ha
km2
```

Conversion examples:

```text
5000 m2 → 5000 m2
50000 m2 → 5 ha
2000000 m2 → 2 km2
```

---

## Shapefile ZIP Validation

A Shapefile normally requires at least:

```text
.shp
.shx
.dbf
```

The application:

1. Validates the ZIP archive.
2. Checks for unsafe ZIP paths.
3. Extracts the archive.
4. Searches for a `.shp` file.
5. Rejects archives containing multiple Shapefiles.
6. Checks required Shapefile components.
7. Reads the validated Shapefile using GeoPandas.

---

## File Storage

Uploaded files are stored using unique physical filenames.

For example:

```text
550e8400-e29b-41d4-a716-446655440000_sample.kml
```

This prevents two uploads with the same original filename from overwriting each other.

The original filename is still preserved in the database and API response.

---

## Database

SQLite is used for persistence.

The application contains two main tables:

```text
files
   |
   | 1
   |
   |------ many
              |
              v
      feature_measurements
```

### files

Stores:

- File ID
- Original filename
- File type
- Processing status
- Feature count
- Source CRS
- Measurement CRS
- Creation timestamp

### feature_measurements

Stores:

- Feature index
- Geometry type
- Feature properties
- Measurement type
- Measurement value
- Measurement unit
- Measurement status

The actual geometries are not stored in the database.

The database schema is automatically initialized when the application starts. This allows the API to run correctly in a fresh environment or Docker container without manually creating the SQLite tables.

---

## Error Handling

Examples of handled errors include:

### 400

Unsupported file type

### 400

Corrupted ZIP

### 400

Missing Shapefile components

### 404

File not found

### 422

Unable to process the uploaded geospatial file

Missing CRS is also explicitly rejected rather than silently guessed.

---

## Testing

The project uses pytest.

Run the complete test suite:

```powershell
pytest -v
```

Current test coverage includes:

- API endpoints
- File validation
- KML processing
- Shapefile processing
- ZIP validation
- Geometry validation
- CRS handling
- Area calculation
- Length calculation
- Unit conversion
- Property extraction
- Measurement summaries
- Error handling
- Duplicate filename handling

Current test result:

```text
33 passed
```

---

## Logging

The application uses Python's standard logging module.

Important processing events are logged, including:

- Starting processing
- Reading KML
- Extracting Shapefile ZIP
- Geospatial processing completed
- File processing completed successfully
- File processing failed

Example:

```text
INFO | app.services.geospatial_service |
Starting processing: filename=sample.kml file_type=KML
```

---

## Design Decisions

### Why FastAPI?

FastAPI provides:

- Automatic OpenAPI documentation
- Request validation
- Simple file uploads
- Type-safe API definitions
- Good performance

### Why GeoPandas?

GeoPandas provides a convenient interface for reading and processing geospatial datasets while integrating with Shapely and PyProj.

### Why Shapely?

Shapely is used for geometry validation and geometry-level measurements.

### Why PyProj?

PyProj is used for CRS handling and coordinate transformation.

### Why SQLite?

SQLite is sufficient for this assessment because the API requires lightweight persistent storage without introducing additional infrastructure.

### Why synchronous processing?

The assessment does not require a background job system. Files are processed synchronously after upload, keeping the architecture simple.

### Why store measurements instead of geometries?

The API needs to return calculated measurements and metadata. Storing measurements keeps the database simple and avoids duplicating potentially large geometry data.

---