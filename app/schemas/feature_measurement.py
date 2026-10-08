from typing import Any

from pydantic import BaseModel, ConfigDict


class FeatureMeasurementResponse(BaseModel):
    id: int
    file_id: str
    feature_index: int
    geometry_type: str
    properties: dict[str, Any] | None = None
    measurement_type: str | None = None
    measurement_value: float | None = None
    measurement_unit: str | None = None
    measurement_status: str

    model_config = ConfigDict(from_attributes=True)