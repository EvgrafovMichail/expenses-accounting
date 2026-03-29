import decimal
from functools import partial
from typing import (
    Annotated,
    Any,
)

from pydantic import (
    BaseModel,
    BeforeValidator,
    field_validator,
)

from expense_accounting.constants import (
    DATE_FORMAT,
    PRECISION,
)
from expense_accounting.utils import check_date_satisfy_given_date_format


class Expense(BaseModel):
    date: Annotated[
        str,
        BeforeValidator(
            partial(check_date_satisfy_given_date_format, date_format=DATE_FORMAT)
        ),
    ]
    category: str
    expense: decimal.Decimal

    @field_validator("expense", mode="before")
    @classmethod
    def ensure_expense_is_decimal(cls, expense_raw: Any) -> decimal.Decimal:
        try:
            expense = decimal.Decimal(expense_raw)

        except (ValueError, TypeError, decimal.DecimalException):
            raise ValueError(
                f"impossible to convert given expense {expense_raw!r} to decimal object"
            ) from None

        return expense.quantize(PRECISION)
