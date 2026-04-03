import calendar
import datetime
import decimal
import math
from enum import Enum
from typing import Final

from expense_accounting.constants import DATE_FORMAT
from expense_accounting.data_models.reports import (
    BarsData,
    TimeSeriesData,
    TimeShiftHint,
)


class OrderType(Enum):
    ASC = "asc"
    AS_IS = "as_is"
    DESC = "desc"


class DataConverter:
    DAYS_STEP: Final[int] = 5

    @classmethod
    def convert_date_to_expense_mapping_to_time_series_data(
        cls,
        date_to_expense: dict[datetime.date, decimal.Decimal],
        *,
        add_hints: bool = True,
    ) -> TimeSeriesData:
        if not date_to_expense:
            return TimeSeriesData()

        date_first = cls._get_first_date_of_month(date_to_expense)
        time_shifts, expenses = cls._get_time_series_core_data(
            date_to_expense=date_to_expense,
            date_first=date_first,
        )
        hints = []

        if add_hints:
            hints = cls._get_time_shift_hints(date_first)

        return TimeSeriesData(
            time_shifts=time_shifts,
            expenses=expenses,
            hints=hints,
        )

    @classmethod
    def convert_category_to_expense_mapping_to_bars_data(
        cls,
        category_to_expense: dict[str, decimal.Decimal],
        *,
        order_type: str | OrderType = OrderType.AS_IS,
        log_scale: bool = False,
    ) -> BarsData:
        if not category_to_expense:
            return BarsData()

        bars_data_pairs = cls._get_bars_data_pairs(
            category_to_expense=category_to_expense,
            order_type=OrderType(order_type),
        )
        expenses, categories = cls._split_pairs_to_different_lists(
            bars_data_pairs=bars_data_pairs,
            log_scale=log_scale,
        )

        return BarsData(
            bar_positions=list(range(len(expenses))),
            expenses=expenses,
            categories=categories,
            log_scale=log_scale,
        )

    @staticmethod
    def _get_first_date_of_month(
        date_to_expense: dict[datetime.date, decimal.Decimal],
    ) -> datetime.date:
        date_random = next(iter(date_to_expense))
        return datetime.date(
            year=date_random.year,
            month=date_random.month,
            day=1,
        )

    @staticmethod
    def _get_time_series_core_data(
        date_to_expense: dict[datetime.date, decimal.Decimal],
        date_first: datetime.date,
    ) -> tuple[list[float], list[decimal.Decimal]]:
        time_shifts = list[float]()
        expenses = list[decimal.Decimal]()

        for date, expense in date_to_expense.items():
            time_shift = (date - date_first).days
            time_shifts.append(time_shift)
            expenses.append(expense)

        return time_shifts, expenses

    @classmethod
    def _get_time_shift_hints(
        cls,
        date_first: datetime.date,
    ) -> list[TimeShiftHint]:
        _, days_amount = calendar.monthrange(
            year=date_first.year,
            month=date_first.month,
        )
        hints = list[TimeShiftHint]()

        for i in range(0, days_amount, cls.DAYS_STEP):
            date_curr = date_first + datetime.timedelta(days=i)
            hint = TimeShiftHint(
                time_shift=i,
                hint=date_curr.strftime(DATE_FORMAT),
            )
            hints.append(hint)

        return hints

    @staticmethod
    def _get_bars_data_pairs(
        category_to_expense: dict[str, decimal.Decimal],
        order_type: OrderType,
    ) -> list[tuple[str, decimal.Decimal]]:
        if order_type is OrderType.AS_IS:
            return list(category_to_expense.items())

        return sorted(
            category_to_expense.items(),
            key=lambda x: x[-1],
            reverse=order_type is OrderType.DESC,
        )

    @classmethod
    def _split_pairs_to_different_lists(
        cls,
        bars_data_pairs: list[tuple[str, decimal.Decimal]],
        log_scale: bool,
    ) -> tuple[list[decimal.Decimal], list[str]]:
        transform_expense = cls._get_log_expense if log_scale else cls._do_nothing
        expenses = list[decimal.Decimal]()
        categories = list[str]()

        for category, expense in bars_data_pairs:
            expenses.append(transform_expense(expense))
            categories.append(category)

        return expenses, categories

    @staticmethod
    def _get_log_expense(expense: decimal.Decimal) -> decimal.Decimal:
        if expense <= 0:
            return expense

        return decimal.Decimal(math.log(expense))

    @staticmethod
    def _do_nothing(expense: decimal.Decimal) -> decimal.Decimal:
        return expense
