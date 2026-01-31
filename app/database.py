import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Pull DB password from environment (fallback to 'secret' for dev)
db_password = os.environ.get("DB_PASSWORD", "secret")
DATABASE_URL = f"postgresql+psycopg://inbody:{quote_plus(db_password)}@localhost:5432/inbody"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
