#!/usr/bin/env python3

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .analytics import rolling_average
from .database import SessionLocal, engine
from . import models, schemas, crud
from datetime import datetime, timedelta, timezone


ALLOWED_FIELDS = {
    "weight_lb",
    "skeletal_muscle_lb",
    "body_fat_lb",
    "body_fat_percent",
    "soft_lean_lb",
    "waist_hip_ratio",
    "visceral_fat_level",
    "inbody_score",
}


app = FastAPI(title="InBody Tracker API")


@app.on_event("startup")
def on_startup():
    """Create DB tables on application startup instead of at import time.

This avoids side-effects when importing `app` (for example when exporting
OpenAPI spec) and ensures tables are created when the server actually runs.
"""
    models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=schemas.UserOut)
def add_user(u: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, u)

@app.post("/metrics", response_model=schemas.InBodyMetricsOut)
def add_metric(
    m: schemas.InBodyMetricsCreate,
    db: Session = Depends(get_db)
):
    if not crud.get_user(db, m.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    # Parse measured_at from flexible format
    try:
        from dateutil import parser

        measured_at = parser.parse(m.measured_at)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid measured_at: {e}")

    if measured_at.tzinfo is None:
        measured_at = measured_at.replace(tzinfo=timezone.utc)

    # Build metric with parsed measured_at
    metric_data = m.model_dump()
    metric_data["measured_at"] = measured_at

    metric = models.InBodyMetrics(**metric_data)
    db.add(metric)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Check if it's a unique constraint violation on (user_id, measured_at)
        if "uix_user_measured_at" in str(e) or "unique" in str(e).lower():
            raise HTTPException(
                status_code=409,
                detail=f"Metric already exists for user {m.user_id} at {measured_at}"
            )
        raise HTTPException(status_code=400, detail="Database constraint violation")
    db.refresh(metric)
    return metric

@app.get("/users/{user_id}/metrics", response_model=list[schemas.InBodyMetricsOut])
def list_user_metrics(user_id: int, db: Session = Depends(get_db)):
    return crud.get_metrics_for_user(db, user_id)

@app.get("/users/{user_id}/metrics/{field}/rolling-average", response_model=schemas.RollingAverageResponse)
def get_rolling_average(
    user_id: int,
    field: str,
    days: int = 7,
    as_of: str | None = None,
    db: Session = Depends(get_db)
):
    # Verify user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if field not in ALLOWED_FIELDS:
        raise HTTPException(status_code=400, detail="Invalid metric")

    # Parse as_of (flexible) or use now
    if as_of is None:
        as_of_dt = datetime.now(timezone.utc)
    else:
        try:
            from dateutil import parser

            as_of_dt = parser.parse(as_of)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid as_of: {e}")

        if as_of_dt.tzinfo is None:
            as_of_dt = as_of_dt.replace(tzinfo=timezone.utc)

    try:
        avg = rolling_average(db, user_id, field, days, as_of_dt)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if avg is None:
        raise HTTPException(status_code=404, detail="No data in window")

    window_start = as_of_dt - timedelta(days=days)

    return schemas.RollingAverageResponse(
        user_id=user_id,
        field=field,
        days=days,
        as_of=as_of_dt,
        window_start=window_start,
        value=round(avg, 2),
    )