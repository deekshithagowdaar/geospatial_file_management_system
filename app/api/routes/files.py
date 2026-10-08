from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.file import File as FileModel
from app.models.feature_measurement import FeatureMeasurement
from app.schemas.file import FileResponse
from app.schemas.measurement import MeasurementSummaryResponse
from app.services.file_storage import save_uploaded_file
from app.services.file_validator import validate_file
from app.services.geospatial_service import process_file


router = APIRouter(
    prefix="/api/files",
    tags=["Files"]
)


@router.post("/", response_model=FileResponse)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    validate_file(file)

    try:
        file_path = save_uploaded_file(file)

        file_record = FileModel(
            filename=file.filename,
            file_type=file_path.suffix.lower().replace(".", "").upper(),
            status="PENDING"
        )

        db.add(file_record)
        db.commit()
        db.refresh(file_record)

        file_record = process_file(
            db,
            file_record,
            file_path
        )

        return file_record

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        )

    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Unable to process the uploaded geospatial file."
        )


@router.get(
    "/{file_id}/",
    response_model=FileResponse
)
def get_file(
    file_id: str,
    db: Session = Depends(get_db)
):
    file_record = db.get(
        FileModel,
        file_id
    )

    if file_record is None:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return file_record


@router.get(
    "/{file_id}/measurements/",
    response_model=MeasurementSummaryResponse
)
def get_measurements(
    file_id: str,
    db: Session = Depends(get_db)
):
    file_record = db.get(
        FileModel,
        file_id
    )

    if file_record is None:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    measurements = (
        db.query(FeatureMeasurement)
        .filter(
            FeatureMeasurement.file_id == file_id
        )
        .order_by(
            FeatureMeasurement.feature_index
        )
        .all()
    )

    measured_features = sum(
        1
        for item in measurements
        if item.measurement_status == "MEASURED"
    )

    not_required_features = sum(
        1
        for item in measurements
        if item.measurement_status == "NOT_REQUIRED"
    )

    unsupported_features = sum(
        1
        for item in measurements
        if item.measurement_status == "UNSUPPORTED"
    )

    failed_features = sum(
        1
        for item in measurements
        if item.measurement_status == "FAILED"
    )

    area_values = [
        item.measurement_value
        for item in measurements
        if item.measurement_type == "area"
        and item.measurement_value is not None
    ]

    length_values = [
        item.measurement_value
        for item in measurements
        if item.measurement_type == "length"
        and item.measurement_value is not None
    ]

    area_unit = None

    for item in measurements:
        if item.measurement_type == "area":
            area_unit = item.measurement_unit
            break

    length_unit = None

    for item in measurements:
        if item.measurement_type == "length":
            length_unit = item.measurement_unit
            break

    total_area = (
        sum(area_values)
        if area_values
        else None
    )

    minimum_area = (
        min(area_values)
        if area_values
        else None
    )

    maximum_area = (
        max(area_values)
        if area_values
        else None
    )

    average_area = (
        total_area / len(area_values)
        if area_values
        else None
    )

    total_length = (
        sum(length_values)
        if length_values
        else None
    )

    minimum_length = (
        min(length_values)
        if length_values
        else None
    )

    maximum_length = (
        max(length_values)
        if length_values
        else None
    )

    average_length = (
        total_length / len(length_values)
        if length_values
        else None
    )

    return {
        "file_id": file_id,
        "total_features": len(measurements),
        "measured_features": measured_features,
        "not_required_features": not_required_features,
        "unsupported_features": unsupported_features,
        "failed_features": failed_features,

        "total_area": total_area,
        "minimum_area": minimum_area,
        "maximum_area": maximum_area,
        "average_area": average_area,
        "area_unit": area_unit,

        "total_length": total_length,
        "minimum_length": minimum_length,
        "maximum_length": maximum_length,
        "average_length": average_length,
        "length_unit": length_unit,

        "measurements": measurements
    }