from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    metrics = relationship(
        "InBodyMetrics",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class InBodyMetrics(Base):
    __tablename__ = "inbody_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    measured_at = Column(DateTime, index=True, nullable=False)

    weight_lb = Column(Float, nullable=False)
    inbody_score = Column(Integer, nullable=False)
    skeletal_muscle_lb = Column(Float, nullable=False)
    body_fat_lb = Column(Float, nullable=False)
    body_fat_percent = Column(Float, nullable=False)

    waist_hip_ratio = Column(Float, nullable=False)
    visceral_fat_level = Column(Integer, nullable=False)

    bmr_kcal = Column(Integer, nullable=False)
    soft_lean_lb = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="metrics")

    __table_args__ = (
        UniqueConstraint("user_id", "measured_at", name="uix_user_measured_at"),
    )
