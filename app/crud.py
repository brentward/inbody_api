from sqlalchemy.orm import Session
from . import models, schemas


def create_user(db: Session, u: schemas.UserCreate):
    user = models.User(**u.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session):
    return db.query(models.User).order_by(models.User.created_at).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_metric(db: Session, m: schemas.InBodyMetricsCreate):
    entry = models.InBodyMetrics(**m.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def get_metrics_for_user(db: Session, user_id: int):
    return (
        db.query(models.InBodyMetrics)
        .filter(models.InBodyMetrics.user_id == user_id)
        .order_by(models.InBodyMetrics.measured_at)
        .all()
    )

def get_all_metrics(db: Session):
    return (
        db.query(models.InBodyMetrics)
        .order_by(models.InBodyMetrics.measured_at)
        .all()
    )