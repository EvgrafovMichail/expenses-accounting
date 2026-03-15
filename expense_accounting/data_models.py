import datetime
import decimal
from typing import (
    Any,
    Final,
)

from pydantic import (
    BaseModel,
    field_validator,
)

from expense_accounting.constants import DATE_FORMAT


PRECISION: Final[decimal.Decimal] = decimal.Decimal(".01")


class Expense(BaseModel):
    date: str
    category: str
    expense: decimal.Decimal

    @field_validator("date", mode="after")
    @classmethod
    def check_date_satisfy_Ymd_date_format(cls, date_str: str) -> str:
        try:
            datetime.datetime.strptime(date_str, DATE_FORMAT)

        except ValueError:
            raise ValueError(
                f"date string {date_str!r} doesn't match date format {DATE_FORMAT!r}"
            ) from None

        return date_str

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
