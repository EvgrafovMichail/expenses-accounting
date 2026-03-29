from typing import Final

import matplotlib.pyplot as plt

from expense_accounting.data_models.reports import TimeSeriesData


class GraphRender:
    COLOR_TIME_SERIES: Final[str] = "#275BF5"

    @classmethod
    def render_time_series_graph(
        cls,
        axis: plt.Axes,
        time_series_data: TimeSeriesData,
    ) -> None:
        cls._set_time_series_texts(
            axis=axis,
            time_series_data=time_series_data,
        )
        cls._set_time_series_graph(
            axis=axis,
            time_series_data=time_series_data,
        )
        cls._set_time_series_grid(
            axis=axis,
            time_shifts=time_series_data.time_shifts,
        )

    @classmethod
    def _set_time_series_texts(
        cls,
        axis: plt.Axes,
        time_series_data: TimeSeriesData,
    ) -> None:
        axis.set_title("Expense per day", fontsize=20, fontweight="bold", c="dimgray")
        axis.set_ylabel("expense, ₽", fontsize=15, fontweight="bold", c="dimgray")

        if not time_series_data.hints:
            return

        tick_positions, tick_labels = cls._get_ticks_data(time_series_data)
        axis.set_xticks(tick_positions, tick_labels, rotation=90)

    @staticmethod
    def _get_ticks_data(
        time_series_data: TimeSeriesData,
    ) -> tuple[list[float], list[str]]:
        tick_positions = list[float]()
        tick_labels = list[str]()

        for hint in time_series_data.hints:
            tick_positions.append(hint.time_shift)
            tick_labels.append(hint.hint)

        return tick_positions, tick_labels

    @classmethod
    def _set_time_series_graph(
        cls,
        axis: plt.Axes,
        time_series_data: TimeSeriesData,
    ) -> None:
        axis.plot(
            time_series_data.time_shifts,
            time_series_data.expenses,
            c=cls.COLOR_TIME_SERIES,
            marker="o",
        )
        axis.fill_between(
            time_series_data.time_shifts,
            time_series_data.expenses,
            color=cls.COLOR_TIME_SERIES,
            alpha=0.3,
        )

    @staticmethod
    def _set_time_series_grid(
        axis: plt.Axes,
        time_shifts: list[float],
    ) -> None:
        axis.set_xlim(min(time_shifts), max(time_shifts))
        axis.set_ylim(0)
        axis.grid()
