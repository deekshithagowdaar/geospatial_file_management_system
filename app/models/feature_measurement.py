from typing import Any

from sqlalchemy import Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class FeatureMeasurement(Base):
    __tablename__ = "feature_measurements"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    file_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False
    )

    feature_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    geometry_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    properties: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True
    )

    measurement_type: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    measurement_value: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    measurement_unit: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    measurement_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    file = relationship(
        "File",
        back_populates="features"
    )