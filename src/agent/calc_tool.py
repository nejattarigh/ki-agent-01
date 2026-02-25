from __future__ import annotations

from typing import Any, Dict
import ast
import operator as op

# Safe calculator (no eval)
_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression")

def calc(expression: str) -> Dict[str, Any]:
    # normalize: allow ^ as power (user habit), convert to Python power operator
    normalized = expression.replace("^", "**")

    try:
        node = ast.parse(normalized, mode="eval").body
        value = _eval(node)
        return {"expression": expression, "normalized": normalized, "value": value}
    except Exception as e:
        return {"error": str(e), "expression": expression, "normalized": normalized}