from pathlib import Path
import shutil
import uuid

from fastapi import UploadFile


UPLOAD_DIR = Path("uploads")


def save_uploaded_file(file: UploadFile) -> Path:
    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    original_filename = Path(file.filename).name

    unique_name = (
        f"{uuid.uuid4()}_{original_filename}"
    )

    file_path = UPLOAD_DIR / unique_name

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return file_path