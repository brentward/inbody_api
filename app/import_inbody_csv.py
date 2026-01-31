#!/usr/bin/env python3

import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import SessionLocal, engine
from app import models

CSV_PATH = "InBody Results Log.csv"

# ---------- helpers ----------

def parse_timestamp(value: str) -> datetime:
    """
    Adjust this if your CSV uses a different format.
    ISO-8601 is preferred.
    """
    try:
        dt = datetime.fromisoformat(value)
    except ValueError:
        # fallback if needed
        dt = datetime.strptime(value, "%d-%b-%y %I:%M %p")

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def get_or_create_user(
    db: Session,
    email: str,
    name: str | None = None
) -> models.User:
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        return user

    user = models.User(email=email, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def metric_exists(
    db: Session,
    user_id: int,
    measured_at: datetime
) -> bool:
    return (
        db.query(models.InBodyMetrics)
        .filter(
            models.InBodyMetrics.user_id == user_id,
            models.InBodyMetrics.measured_at == measured_at,
        )
        .first()
        is not None
    )

# ---------- main import ----------

def main():
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    
    df = pd.read_csv(CSV_PATH)

    required_columns = {
        "user_email",
        "timestamp",
        "weight_lb",
        "skeletal_muscle_lb",
        "body_fat_lb",
        "body_fat_percent",
        "waist_hip_ratio",
        "visceral_fat_level",
        "bmr_kcal",
        "soft_lean_lb",
        "inbody_score",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise RuntimeError(f"Missing required CSV columns: {missing}")

    db = SessionLocal()

    inserted = 0
    skipped = 0
    users_created = 0

    for _, row in df.iterrows():
        user = get_or_create_user(
            db,
            name=row.get("user_name"),
            email=row["user_email"],
        )

        ts = parse_timestamp(row["timestamp"])

        if metric_exists(db, user.id, ts):
            skipped += 1
            continue

        m = models.InBodyMetrics(
            user_id=user.id,
            measured_at=ts,            
            inbody_score=int(row["inbody_score"]),
            weight_lb=float(row["weight_lb"]),
            skeletal_muscle_lb=float(row["skeletal_muscle_lb"]),
            body_fat_lb=float(row["body_fat_lb"]),
            body_fat_percent=float(row["body_fat_percent"]),
            waist_hip_ratio=float(row["waist_hip_ratio"]),
            visceral_fat_level=int(row["visceral_fat_level"]),
            bmr_kcal=int(row["bmr_kcal"]),
            soft_lean_lb=float(row["soft_lean_lb"]),

        )

        db.add(m)
        inserted += 1

    db.commit()
    db.close()

    print("Import complete")
    print(f"  Metrics inserted: {inserted}")
    print(f"  Metrics skipped : {skipped}")

if __name__ == "__main__":
    main()
