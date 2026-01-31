from __future__ import annotations
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine

from alembic import context

# ensure repo root is on sys.path so 'app' can be imported
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Prefer DATABASE_URL env var; fall back to app.database if present
db_url = os.getenv("DATABASE_URL")
if not db_url:
    try:
        from app import database

        db_url = getattr(database, "DATABASE_URL", None)
    except Exception:
        db_url = None

if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# import target metadata from the application
try:
    from app import models

    target_metadata = models.Base.metadata
except Exception:
    try:
        from app.database import Base

        target_metadata = Base.metadata
    except Exception:
        target_metadata = None


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = None
    # if the app exposes an engine, use it; otherwise create one from config
    try:
        from app.database import engine as app_engine

        connectable = app_engine
    except Exception:
        connectable = create_engine(config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
