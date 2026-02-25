from __future__ import annotations

from typing import List
from .repo_tool import search_in_repo
from .sql_tool import run_sql
from .calc_tool import calc
import operator as op

TOOLS = {
    "calc": calc,
    "search_in_repo": search_in_repo,
    "run_sql": run_sql,
}

TOOL_SPECS: List[dict] = [
    {
        "type": "function",
        "function": {
            "name": "calc",
            "description": "Safely evaluate a simple math expression like 2*(3+4).",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"},
                },
                "required": ["expression"],
            },
        },
    }
]
TOOL_SPECS.append(
    {
        "type": "function",
        "function": {
            "name": "search_in_repo",
            "description": "Search for a string in repository files and return matching file previews.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_hits": {"type": "integer", "default": 10},
                },
                "required": ["query"],
            },
        },
    }
)
TOOL_SPECS.append(
    {
        "type": "function",
        "function": {
            "name": "run_sql",
            "description": "Run a SELECT query on SQL Server and return rows (limited).",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    }
)