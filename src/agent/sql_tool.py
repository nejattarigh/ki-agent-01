from __future__ import annotations

import os
from typing import Any, Dict, List

import pyodbc
from dotenv import load_dotenv
import datetime
import decimal
import uuid

load_dotenv()

ROW_LIMIT = 50


def _get_conn_str() -> str:
    cs = os.getenv("SQL_CONN", "").strip()
    if not cs:
        raise RuntimeError("SQL_CONN fehlt in .env")
    return cs


def run_sql(query: str) -> Dict[str, Any]:
    q = query.strip()
    q_l = q.lower()

    # Guardrail: only SELECT
    if not q_l.startswith("select"):
        return {"error": "Only SELECT queries allowed."}

    try:
        with pyodbc.connect(_get_conn_str(), timeout=5) as conn:
            cur = conn.cursor()
            cur.execute(q)

            cols = [c[0] for c in cur.description] if cur.description else []
            rows = cur.fetchmany(ROW_LIMIT) if cols else []
            def _safe(v):
                if isinstance(v, (datetime.datetime, datetime.date, datetime.time)):
                    return v.isoformat()
                if isinstance(v, decimal.Decimal):
                    return float(v)
                if isinstance(v, uuid.UUID):
                    return str(v)
                return v

            return {
                "columns": cols,
                "rows": [[_safe(v) for v in r] for r in rows],
                "row_limit": ROW_LIMIT,
            }
    except Exception as e:
        return {"error": str(e)}