from fastapi import APIRouter, Depends

from ..dependencies import get_history
from ..schemas import CalculatorLog


router = APIRouter()


@router.get(
    "/history",
    response_model=list[CalculatorLog],
)
def get_history_route(
    history=Depends(get_history),
):
    return list(history)


@router.delete("/history")
def clear_history(
    history=Depends(get_history),
):
    history.clear()

    return {
        "ok": True
    }