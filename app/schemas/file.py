from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FileResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    status: str
    feature_count: int
    source_crs: str | None = None
    measurement_crs: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)