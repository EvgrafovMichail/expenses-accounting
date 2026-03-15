import pathlib
from typing import Final

import pandas as pd

from expense_accounting.constants import MONTH_FORMAT
from expense_accounting.data_models import Expense
from expense_accounting.exceptions import DataLoaderError
from expense_accounting.utils import check_date_satisfy_given_date_format


class DataLoaderCSV:
    CSV_SUFFIX: Final[str] = "csv"
    DEFAULT_PATH_TO_FILES: Final[str] = "./"
    DEFAULT_SEPARATOR: Final[str] = ";"

    _path_to_files: pathlib.Path
    _separator: str

    def __init__(
        self,
        path_to_files: str | pathlib.Path = DEFAULT_PATH_TO_FILES,
        separator: str = DEFAULT_SEPARATOR,
    ) -> None:
        if isinstance(path_to_files, str):
            path_to_files = pathlib.Path(path_to_files)

        if not path_to_files.exists():
            raise DataLoaderError(
                f"folder with expense reports doesn't exist: {path_to_files}"
            )

        if not separator:
            raise ValueError("separator value must be non-empty")

        self._path_to_files = path_to_files
        self._separator = separator

    def load_data(self, date_str: str) -> list[Expense]:
        path_to_expense_report = self._get_path_to_expense_report(date_str=date_str)
        return self._read_expenses_from_csv_file(
            path_to_expense_report=path_to_expense_report,
        )

    def _get_path_to_expense_report(self, date_str: str) -> pathlib.Path:
        date_str = check_date_satisfy_given_date_format(
            date_str=date_str,
            date_format=MONTH_FORMAT,
        )
        filename = f"{date_str}.{self.CSV_SUFFIX}"
        path_to_expense_report = self._path_to_files / filename

        if not path_to_expense_report.exists():
            raise DataLoaderError(f"expense record for date {date_str!r} doesn't exist")

        return path_to_expense_report

    def _read_expenses_from_csv_file(
        self,
        path_to_expense_report: pathlib.Path,
    ) -> list[Expense]:
        expense_report = pd.read_csv(path_to_expense_report, sep=self._separator)
        expenses = list[Expense]()

        for _, row in expense_report.iterrows():
            row_as_dict = row.to_dict()
            expenses.append(Expense(**row_as_dict))  # type: ignore

        return expenses
