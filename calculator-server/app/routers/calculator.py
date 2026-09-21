from collections import deque
from datetime import datetime
import math

from asteval import Interpreter
from fastapi import APIRouter, Depends

from app.dependencies import expand_percent, get_history
from app.schemas import CalculatorLog, ExpressionIn

router = APIRouter()

aeval = Interpreter(
    minimal=True,
    usersyms={
        "pi": math.pi,
        "e": math.e,
    },
)


@router.post("/calculate")
def calculate(
    expression: ExpressionIn,
    code: str = Depends(expand_percent),
    history: deque = Depends(get_history),
):
    try:
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {
                "ok": False,
                "expr": expression.expr,
                "result": "",
                "error": msg,
            }

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        log_entry = CalculatorLog(
            timestamp=datetime.now(),
            expr=expression.expr,
            result=result,
        )
        history.appendleft(log_entry)

        return {
            "ok": True,
            "expr": expression.expr,
            "result": result,
            "error": "",
        }
    except Exception as e:
        return {
            "ok": False,
            "expr": expression.expr,
            "result": "",
            "error": str(e),
        }
