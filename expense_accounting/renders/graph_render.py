from collections.abc import Sequence
from typing import (
    Callable,
    Final,
    TypeVar,
)

import matplotlib.pyplot as plt

from expense_accounting.data_models.reports import (
    BarsData,
    TimeSeriesData,
)


T = TypeVar("T")


class GraphRender:
    COLOR_TIME_SERIES: Final[str] = "#275BF5"
    FONTSIZE_TITLE: Final[int] = 20
    FONTSIZE_LABEL: Final[int] = 15
    ROTATION: Final[int] = 90
    TEXT_SETTINGS_COMMON: Final[dict[str, str]] = {
        "fontweight": "bold",
        "c": "dimgray",
    }

    @classmethod
    def render_time_series_graph(
        cls,
        axis: plt.Axes,
        time_series_data: TimeSeriesData,
    ) -> None:
        cls._set_up_graph(
            axis=axis,
            graph_data=time_series_data,
            graph_setters=(
                cls._set_time_series_texts,
                cls._set_time_series_graph,
                cls._set_time_series_grid,
            ),
        )

    @classmethod
    def render_bars_graph(
        cls,
        axis: plt.Axes,
        bars_data: BarsData,
    ) -> None:
        cls._set_up_graph(
            axis=axis,
            graph_data=bars_data,
            graph_setters=(
                cls._set_bars_texts,
                cls._set_bars_graph,
            ),
        )

    @classmethod
    def _set_time_series_texts(
        cls,
        axis: plt.Axes,
        time_series_data: TimeSeriesData,
    ) -> None:
        axis.set_title(
            "Expense per day",
            fontsize=cls.FONTSIZE_TITLE,
            **cls.TEXT_SETTINGS_COMMON,
        )
        axis.set_ylabel(
            "expense, ₽",
            fontsize=cls.FONTSIZE_LABEL,
            **cls.TEXT_SETTINGS_COMMON,
        )

        if not time_series_data.hints:
            return

        tick_positions, tick_labels = cls._get_ticks_data(time_series_data)
        axis.set_xticks(tick_positions, tick_labels, rotation=cls.ROTATION)

    @classmethod
    def _set_bars_texts(
        cls,
        axis: plt.Axes,
        bars_data: BarsData,
    ) -> None:
        axis.set_title(
            "Expense per category",
            fontsize=cls.FONTSIZE_TITLE,
            **cls.TEXT_SETTINGS_COMMON,
        )
        ylabel = "log expense, ln(₽)" if bars_data.log_scale else "expense, ₽"
        axis.set_ylabel(
            ylabel,
            fontsize=cls.FONTSIZE_LABEL,
            **cls.TEXT_SETTINGS_COMMON,
        )

        axis.set_xticks(
            bars_data.bar_positions, bars_data.categories, rotation=cls.ROTATION
        )

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

    @classmethod
    def _set_bars_graph(
        cls,
        axis: plt.Axes,
        bars_data: BarsData,
    ) -> None:
        axis.bar(
            bars_data.bar_positions,
            bars_data.expenses,
            color="#459DFB",
            edgecolor="#163EB5",
        )
        axis.grid()

    @staticmethod
    def _set_time_series_grid(
        axis: plt.Axes,
        time_series_data: TimeSeriesData,
    ) -> None:
        axis.set_xlim(
            min(time_series_data.time_shifts),
            max(time_series_data.time_shifts),
        )
        axis.set_ylim(0)
        axis.grid()

    @staticmethod
    def _set_up_graph(
        axis: plt.Axes,
        graph_data: T,
        graph_setters: Sequence[Callable[[plt.Axes, T], None]],
    ) -> None:
        for graph_setter in graph_setters:
            graph_setter(axis, graph_data)
