from datetime import datetime
from pydantic import BaseModel


class BaseExpression(BaseModel):
    expr: str


class ExpressionIn(BaseModel):
    expr: str


class ExpressionOut(ExpressionIn):
    timestamp: datetime
    result: float | int | str


class CalculatorLog(ExpressionOut):
    pass


Expression = ExpressionIn