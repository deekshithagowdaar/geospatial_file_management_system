from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.core.config import settings


ALLOWED_EXTENSIONS = {".kml", ".zip"}


def validate_file(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Only KML and ZIP files are allowed."
        )

    max_size = settings.max_upload_size_mb * 1024 * 1024

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > max_size:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds the maximum limit of {settings.max_upload_size_mb} MB."
        )