import datetime
import decimal
from collections import defaultdict
from collections.abc import Sequence

from expense_accounting.constants import (
    DATE_FORMAT,
    PRECISION,
)
from expense_accounting.data_models import Expense


class DataAggregatorBasic:
    @staticmethod
    def get_total_expense(expenses: Sequence[Expense]) -> decimal.Decimal:
        return sum(
            (expense.expense for expense in expenses),
            start=decimal.Decimal(),
        )

    @staticmethod
    def get_expense_per_category(
        expenses: Sequence[Expense],
    ) -> dict[str, decimal.Decimal]:
        category_to_expense = defaultdict[str, decimal.Decimal](decimal.Decimal)

        for expense in expenses:
            category_to_expense[expense.category] += expense.expense

        return dict(category_to_expense)

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
