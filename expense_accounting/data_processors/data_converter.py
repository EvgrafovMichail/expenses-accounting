import calendar
import datetime
import decimal
from typing import Final

from expense_accounting.constants import DATE_FORMAT
from expense_accounting.data_models.reports import (
    TimeSeriesData,
    TimeShiftHint,
)


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
