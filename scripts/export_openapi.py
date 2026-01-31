#!/usr/bin/env python3
"""Export the FastAPI OpenAPI spec to openapi.json for Postman import.

Usage:
  python scripts/export_openapi.py

Then import `openapi.json` into Postman (Import → File), or convert to
Postman collection JSON with the `openapi2postmanv2` tool:

  # install (if needed)
  npm install -g openapi-to-postmanv2

  # convert
  openapi2postmanv2 -s openapi.json -o postman_collection.json -p

"""
import json
import sys
from pathlib import Path

# Ensure project root is on sys.path when running this script from scripts/
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.main import app


def main() -> None:
    spec = app.openapi()
    out = Path("openapi.json")
    out.write_text(json.dumps(spec, indent=2))
    print(f"Wrote OpenAPI spec to {out.resolve()}")


if __name__ == "__main__":
    main()
