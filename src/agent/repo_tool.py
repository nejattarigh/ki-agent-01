from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


def search_in_repo(query: str, max_hits: int = 10) -> Dict[str, Any]:
    query_l = query.lower().strip()
    if not query_l:
        return {"error": "query is empty"}

    hits: List[Dict[str, str]] = []
    root = Path(".")

    for p in root.rglob("*"):
        if p.is_dir():
            continue

        sp = str(p)
        if any(part in sp for part in [".venv", ".git", "__pycache__", ".ruff_cache", ".pytest_cache"]):
            continue

        # keep it simple: only scan small-ish text files
        if p.suffix.lower() not in {".py", ".toml", ".md", ".txt", ".env", ".yaml", ".yml", ".json"}:
            continue

        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        idx = text.lower().find(query_l)
        if idx != -1:
            preview = text[max(0, idx - 120) : min(len(text), idx + len(query) + 120)].replace("\n", " ")
            hits.append({"file": sp, "preview": preview})
            if len(hits) >= max_hits:
                break

    return {"query": query, "hits": hits, "count": len(hits)}