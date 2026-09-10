import re

# เติม (?<!%) เพื่อไม่ให้จับตัวเลขที่มี % ติดอยู่ เช่น "10%" จะไม่ถูกมองเป็นตัวเลข a
_percent_pair = re.compile(r"""
    (?<!%)(?P<a>\b\d+(?:\.\d+)?\b)
    \s*(?P<op>[+\-*/])\s*
    (?P<b>\d+(?:\.\d+)?)%
""", re.VERBOSE)

_number_percent = re.compile(r"(?P<n>\d+(?:\.\d+)?)%")

def expand_percent(expr: str) -> str:
    """Handle A op B% and standalone N% patterns."""
    s = expr
    
    # 1. จัดการคู่ A op B% เฉพาะกรณีที่ A เป็นตัวเลขธรรมดา (ไม่มี %)
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
        s = s[:m.start()] + repl + s[m.end():]

    # 2. จัดการตัวเลขที่มี % ที่เหลือทั้งหมด (Standalone % เช่น 100% หรือ 10% + 20%)
    s = _number_percent.sub(lambda m: f"({m.group('n')}/100)", s)
    
    return s