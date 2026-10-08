import logging
from pathlib import Path

from sqlalchemy.orm import Session

from app.geospatial.processor import (
    process_kml,
    process_shapefile
)
from app.geospatial.shapefile import extract_shapefile_zip
from app.models.feature_measurement import FeatureMeasurement
from app.models.file import File


logger = logging.getLogger(__name__)


def process_file(
    db: Session,
    file_record: File,
    file_path: str | Path
) -> File:

    file_path = Path(file_path)

    logger.info(
        "Starting processing: filename=%s file_type=%s file_id=%s",
        file_record.filename,
        file_record.file_type,
        file_record.id
    )

    file_record.status = "PROCESSING"
    db.commit()

    try:
        if file_record.file_type == "KML":

            logger.info(
                "Reading KML file: %s",
                file_path
            )

            result = process_kml(file_path)

        elif file_record.file_type == "ZIP":

            logger.info(
                "Extracting Shapefile ZIP: %s",
                file_path
            )

            extract_dir = (
                file_path.parent /
                f"{file_path.stem}_extracted"
            )

            shapefile_path = extract_shapefile_zip(
                file_path,
                extract_dir
            )

            logger.info(
                "Shapefile found: %s",
                shapefile_path
            )

            result = process_shapefile(
                shapefile_path
            )

        else:
            raise ValueError(
                f"Unsupported file type: {file_record.file_type}"
            )

        logger.info(
            "Geospatial processing completed: "
            "features=%s source_crs=%s measurement_crs=%s",
            result["feature_count"],
            result["source_crs"],
            result["measurement_crs"]
        )

        file_record.feature_count = result["feature_count"]
        file_record.source_crs = result["source_crs"]
        file_record.measurement_crs = result["measurement_crs"]

        for measurement in result["measurements"]:

            feature = FeatureMeasurement(
                file_id=file_record.id,
                feature_index=measurement["feature_index"],
                geometry_type=measurement["geometry_type"],
                properties=measurement["properties"],
                measurement_type=measurement["measurement_type"],
                measurement_value=measurement["measurement_value"],
                measurement_unit=measurement["measurement_unit"],
                measurement_status=measurement["measurement_status"]
            )

            db.add(feature)

        file_record.status = "COMPLETED"

        db.commit()
        db.refresh(file_record)

        logger.info(
            "File processing completed successfully: "
            "file_id=%s status=%s",
            file_record.id,
            file_record.status
        )

        return file_record

    except Exception:
        db.rollback()

        file_record.status = "FAILED"
        db.commit()

        logger.exception(
            "File processing failed: file_id=%s filename=%s",
            file_record.id,
            file_record.filename
        )

        raise