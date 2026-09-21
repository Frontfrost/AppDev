from datetime import datetime
from pydantic import BaseModel


class BaseExpression(BaseModel):
    expr: str


class ExpressionIn(BaseExpression):
    pass


class ExpressionOut(ExpressionIn):
    timestamp: datetime
    result: float | int | str


class CalculatorLog(ExpressionOut):
    pass


# Aliases for backward compatibility and assignment requirements
Expression = ExpressionIn
