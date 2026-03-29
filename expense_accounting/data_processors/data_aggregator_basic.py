import datetime
import decimal
from collections import defaultdict
from collections.abc import Sequence
from typing import (
    Callable,
    TypeVar,
)

from expense_accounting.constants import (
    DATE_FORMAT,
    PRECISION,
)
from expense_accounting.data_models import Expense


T = TypeVar("T")


class DataAggregatorBasic:
    @staticmethod
    def get_total_expense(expenses: Sequence[Expense]) -> decimal.Decimal:
        return sum(
            (expense.expense for expense in expenses),
            start=decimal.Decimal(),
        )

    @classmethod
    def get_expense_per_category(
        cls,
        expenses: Sequence[Expense],
    ) -> dict[str, decimal.Decimal]:
        return cls._sum_up_expenses_grouped_by_key(
            expenses=expenses,
            key=lambda expense: expense.category,
        )

    @classmethod
    def get_expense_per_date(
        cls,
        expenses: Sequence[Expense],
    ) -> dict[datetime.date, decimal.Decimal]:
        return cls._sum_up_expenses_grouped_by_key(
            expenses=expenses,
            key=lambda expense: cls._convert_date_str_to_date(expense.date),
        )

    @classmethod
    def get_avg_daily_expense(cls, expenses: Sequence[Expense]) -> decimal.Decimal:
        if not expenses:
            return decimal.Decimal()

        date_from = cls._convert_date_str_to_date(expenses[0].date)
        date_to = cls._convert_date_str_to_date(expenses[0].date)
        expense_total = expenses[0].expense

        for i in range(1, len(expenses)):
            expense_total += expenses[i].expense
            date_expense = cls._convert_date_str_to_date(expenses[i].date)

            if date_expense < date_from:
                date_from = date_expense

            if date_to < date_expense:
                date_to = date_expense

        days_amount = (date_to - date_from).days + 1
        return (expense_total / days_amount).quantize(PRECISION)

    @staticmethod
    def _convert_date_str_to_date(date_str: str) -> datetime.date:
        return datetime.datetime.strptime(date_str, DATE_FORMAT).date()

    @staticmethod
    def _sum_up_expenses_grouped_by_key(
        expenses: Sequence[Expense],
        key: Callable[[Expense], T],
    ) -> dict[T, decimal.Decimal]:
        key_to_expense = defaultdict[T, decimal.Decimal](decimal.Decimal)

        for expense in expenses:
            key_value = key(expense)
            key_to_expense[key_value] += expense.expense

        return dict(key_to_expense)
