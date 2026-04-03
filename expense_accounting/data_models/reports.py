# TODO: strange module name, needs to be renamed
import decimal

from pydantic import BaseModel


class TimeShiftHint(BaseModel):
    time_shift: float
    hint: str


# TODO: add validation
class TimeSeriesData(BaseModel):
    time_shifts: list[float] = []
    expenses: list[decimal.Decimal] = []
    hints: list[TimeShiftHint] = []


# TODO: add validation
class BarsData(BaseModel):
    bar_positions: list[float] = []
    expenses: list[decimal.Decimal] = []
    categories: list[str] = []
    log_scale: bool = False
