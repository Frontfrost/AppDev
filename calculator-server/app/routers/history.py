from collections import deque
from fastapi import APIRouter, Depends

from app.dependencies import get_history
from app.schemas import CalculatorLog

router = APIRouter()


@router.get("/history", response_model=list[CalculatorLog])
def get_history_route(history: deque = Depends(get_history)):
    return list(history)


@router.delete("/history")
def clear_history(history: deque = Depends(get_history)):
    history.clear()
    return {"ok": True}
