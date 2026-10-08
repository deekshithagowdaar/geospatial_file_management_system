from pydantic import BaseModel

from app.schemas.feature_measurement import FeatureMeasurementResponse


class MeasurementSummaryResponse(BaseModel):
    file_id: str

    total_features: int
    measured_features: int
    not_required_features: int
    unsupported_features: int
    failed_features: int

    total_area: float | None = None
    minimum_area: float | None = None
    maximum_area: float | None = None
    average_area: float | None = None
    area_unit: str | None = None

    total_length: float | None = None
    minimum_length: float | None = None
    maximum_length: float | None = None
    average_length: float | None = None
    length_unit: str | None = None

    measurements: list[FeatureMeasurementResponse]