from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    name: str | None = None
    
class UserOut(UserCreate):
    id: int

    class Config:
        orm_mode = True

class InBodyMetricsBase(BaseModel):
    weight_lb: float
    inbody_score: int | None = None
    skeletal_muscle_lb: float | None = None
    body_fat_lb: float | None = None
    body_fat_percent: float | None = None
    waist_hip_ratio: float | None = None
    visceral_fat_level: int | None = None
    bmr_kcal: int | None = None
    soft_lean_lb: float | None = None

class InBodyMetricsCreate(BaseModel):
    """Accept measured_at as flexible string format; will be parsed server-side."""
    user_id: int
    measured_at: str  # Accept human-readable or ISO format; parsed in endpoint
    weight_lb: float
    inbody_score: int | None = None
    skeletal_muscle_lb: float | None = None
    body_fat_lb: float | None = None
    body_fat_percent: float | None = None
    waist_hip_ratio: float | None = None
    visceral_fat_level: int | None = None
    bmr_kcal: int | None = None
    soft_lean_lb: float | None = None

class InBodyMetricsOut(InBodyMetricsBase):
    measured_at: datetime
    id: int
    user_id: int

    class Config:
        orm_mode = True


class RollingAverageResponse(BaseModel):
    user_id: int
    field: str
    days: int
    as_of: datetime
    window_start: datetime
    value: float
