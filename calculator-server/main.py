from collections import deque
from datetime import datetime
import math
from asteval import Interpreter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# นำเข้า Pydantic models ที่เพิ่งสร้าง
from models import CalculatorLog, Expression

HISTORY_MAX = 1000
# กำหนด type hint เป็น CalculatorLog
history: deque[CalculatorLog] = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


# 4.a: เปลี่ยนมารับ Expression object แทน str ธรรมดา
@app.post("/calculate")
def calculate(expression: Expression):
    try:
        # เรียก method expand_percent() จาก Expression object โดยตรง
        code = expression.expand_percent()
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

        # บันทึกลง history ในรูปแบบ CalculatorLog
        log_entry = CalculatorLog(
            timestamp=datetime.now(), expr=expression.expr, result=result
        )
        history.appendleft(log_entry)

        return {
            "ok": True,
            "expr": expression.expr,
            "result": result,
            "error": "",
        }
    except Exception as e:
        return {"ok": False, "expr": expression.expr, "error": str(e)}


# 4.b: กำหนด response_model ให้ส่งกลับเป็น list[CalculatorLog]
@app.get("/history", response_model=list[CalculatorLog])
def get_history():
    return list(history)


@app.delete("/history")
def clear_history():
    history.clear()
    return {"ok": True}