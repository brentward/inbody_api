# Copilot / AI Agent Instructions for inbody_api

Purpose: give an AI coding agent the immediate, actionable knowledge to be productive editing and extending this repo.

1) Big picture
- FastAPI service in `app/main.py` exposing user and metric endpoints and a rolling-average helper.
- SQLite + SQLAlchemy for persistence (`app/database.py`, `inbody.db` file). Models live in `app/models.py` and are simple relational tables for `User` and `InBodyMetrics`.
- CRUD helpers are in `app/crud.py`. Data validation/serialization uses Pydantic models in `app/schemas.py`.
- A standalone CSV import script is `app/import_inbody_csv.py` which reads `InBody Results Log.csv` with pandas and inserts metrics.

2) How to run and common developer commands
- Install deps: `pip install -r requirements.txt` (project uses Pydantic v2-style `model_dump()`).
- Run the API server: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` from the repo root.
- Import CSV data: `python -m app.import_inbody_csv` or `python app/import_inbody_csv.py` from repo root.
- The schema tables are created on startup: `models.Base.metadata.create_all(bind=engine)` is called in `app/main.py`.

3) Project-specific conventions & patterns
- DB sessions: use `SessionLocal()` and the `get_db()` FastAPI dependency in new endpoints: `db: Session = Depends(get_db)`.
- CRUD functions commit and `refresh()` objects before returning; follow this pattern for writes.
- Pydantic usage: schemas use `orm_mode` and code uses `model_dump()` (Pydantic v2). Keep that style when constructing models from Pydantic objects.
- Datetimes: models use timezone-aware defaults (`datetime.now(timezone.utc)`). Code in `import_inbody_csv.py` prefers ISO-8601 and falls back to a custom format.
- Naming convention: measurement data is called a "metric" throughout the API and models (`InBodyMetrics`, `POST /metrics`, `get_metrics_for_user()`).

4) Important, discoverable gotchas (do not change silently)
- Timestamp uniqueness: `InBodyMetrics.timestamp` had a global `unique=True` constraint that was removed to allow multiple users to have metrics at the same timestamp. The table-level `UniqueConstraint('user_id','timestamp')` remains to enforce per-user uniqueness.
- CSV import required columns: the importer expects these exact column names: `user_email, timestamp, weight_lb, skeletal_muscle_lb, body_fat_lb, body_fat_percent, waist_hip_ratio, visceral_fat_level, bmr_kcal, soft_lean_lb, inbody_score`.

5) Files to inspect for changes (examples)
- API routes and app startup: app/main.py
- DB config and Base: app/database.py (routes: `POST /metrics`, `GET /users/{user_id}/metrics`)
- DB config and Base: app/database.py
- ORM models and constraints: app/models.py (`InBodyMetrics` class, `inbody_metrics` table)
- Schemas (Pydantic): app/schemas.py (`InBodyMetricsCreate`, `InBodyMetricsOut`)
- CRUD patterns: app/crud.py (`create_metric()`, `get_metrics_for_user()`, `get_all_metrics()`)cs.py (use `VALID_FIELDS` mapping when adding analytics fields)
- CSV importer: app/import_inbody_csv.py

6) Suggested PR checklist for contributors / agents
- If modifying models: explain migration approach (this repo has no migrations; document how to run `create_all` or add alembic).
- Run `python -m app.import_inbody_csv` (with a copy of the CSV) to validate ingestion changes.
- Run the FastAPI server and exercise endpoints (use `uvicorn app.main:app --reload`).
- Preserve existing response models (`response_model=...`) and `orm_mode` where used.

7) When to ask the human
- Any schema/model change that requires data migration or may alter uniqueness constraints.
- Ambiguities in CSV timestamp formats or if adding new CSV columns.
- If adding external services (auth, third-party APIs) — list required secrets and endpoints.

If any section is unclear or you'd like examples (curl requests, sample CSV rows, or a fix PR for the route/timestamp issues), say which area to expand and I will update this file.
