from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from .models import InBodyMetrics


VALID_FIELDS = {
    "weight_lb": InBodyMetrics.weight_lb,
    "skeletal_muscle_lb": InBodyMetrics.skeletal_muscle_lb,
    "body_fat_lb": InBodyMetrics.body_fat_lb,
    "body_fat_percent": InBodyMetrics.body_fat_percent,
    "soft_lean_lb": InBodyMetrics.soft_lean_lb,
    "waist_hip_ratio": InBodyMetrics.waist_hip_ratio,
    "visceral_fat_level": InBodyMetrics.visceral_fat_level,
    "inbody_score": InBodyMetrics.inbody_score,
}

def rolling_average(
    db: Session,
    user_id: int,
    field: str,
    days: int = 7,
    as_of: datetime | None = None
):
    """Compute rolling average for a field over N days ending at as_of (inclusive).
    
    Translates to SQL like:
      SELECT AVG(field) FROM inbody_metrics
      WHERE user_id = ? AND measured_at <= ? AND measured_at >= ? AND field IS NOT NULL
    """
    if field not in VALID_FIELDS:
        raise ValueError(f"Invalid field: {field}")

    if as_of is None:
        as_of = datetime.now(timezone.utc)

    window_start = as_of - timedelta(days=days)

    avg = (
        db.query(func.avg(VALID_FIELDS[field]))
        .filter(InBodyMetrics.user_id == user_id)
        .filter(InBodyMetrics.measured_at >= window_start)
        .filter(InBodyMetrics.measured_at <= as_of)
        .filter(VALID_FIELDS[field] != None)
        .scalar()
    )

    return avg
