import re
from datetime import datetime
from pydantic import BaseModel

# Regex สำหรับคำนวณ %
_percent_pair = re.compile(
    r"""
    (?<!%)(?P<a>\b\d+(?:\.\d+)?\b)
    \s*(?P<op>[+\-*/])\s*
    (?P<b>\d+(?:\.\d+)?)%
""",
    re.VERBOSE,
)
_number_percent = re.compile(r"(?P<n>\d+(?:\.\d+)?)%")


class Expression(BaseModel):
    expr: str

    def expand_percent(self) -> str:
        s = self.expr
        while True:
            m = _percent_pair.search(s)
            if not m:
                break
            a, op, b = m.group("a", "op", "b")
            if op in "+-":
                repl = f"{a} {op} (({b}/100)*{a})"
            elif op == "*":
                repl = f"{a} * ({b}/100)"
            else:
                repl = f"{a} / ({b}/100)"
            s = s[: m.start()] + repl + s[m.end() :]

        s = _number_percent.sub(lambda m: f"({m.group('n')}/100)", s)
        return s


class CalculatorLog(BaseModel):
    timestamp: datetime
    expr: str
    result: float | int | str