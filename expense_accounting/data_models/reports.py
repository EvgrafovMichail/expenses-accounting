# TODO: strange module name, needs to be renamed
import decimal

from pydantic import BaseModel


class TimeShiftHint(BaseModel):
    time_shift: float
    hint: str


class TimeSeriesData(BaseModel):
    time_shifts: list[float] = []
    expenses: list[decimal.Decimal] = []
    hints: list[TimeShiftHint] = []
