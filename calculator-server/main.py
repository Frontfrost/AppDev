from collections import deque
from datetime import datetime
import math
from asteval import Interpreter
from calculator import expand_percent
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

HISTORY_MAX = 1000
# เก็บประวัติการคำนวณในหน่วยความจำ
history = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

# เปิด CORS เพื่อให้ Frontend ยิงข้ามพอร์ตได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@app.post("/calculate")
def calculate(expr: str):
    try:
        code = expand_percent(expr)
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr, "result": "", "error": msg}

        # แปลงเป็น int หากค่าเป็นจำนวนเต็มทศนิยม .0
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        # บันทึกประวัติ
        history.appendleft(
            {
                "expr": expr,
                "result": result,
                "timestamp": datetime.now().isoformat(),
            }
        )

        return {"ok": True, "expr": expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr, "error": str(e)}


@app.get("/history")
def get_history():
    return list(history)


@app.delete("/history")
def clear_history():
    history.clear()
    return {"ok": True}

