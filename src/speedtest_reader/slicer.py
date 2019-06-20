# -*- coding: utf-8 -*-
"""
tbd
"""
import logging
import time

from speedtest_reader import reader

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def slice_input(source, start, end, tz=None):
    """Slice input df using start and end."""

    # ACCCESS DATAFRAME
    df = reader.get_df(source, tz=tz)

    s_pt = time.process_time()
    s_pc = time.perf_counter()

    # _logger.debug(f"{start} is lower bound of slice")
    # _logger.debug(f"{end} is upper bound of slice")

    mask = df.set_index("Timestamp")

    # Find index values for slicing.
    lower = mask.index.searchsorted(start)
    upper = mask.index.searchsorted(end)

    # Slice according to values.
    if start:
        if end:
            df = mask.iloc[lower:upper]
        else:
            df = mask.iloc[lower:]
    else:
        if end:
            df = mask.iloc[:upper]
        else:
            df = mask

    # _logger.debug(f"{df.index.min()} is min index in DataFrame")
    # _logger.debug(f"{df.index.max()} is max index in DataFrame")

    e_pt = time.process_time()
    e_pc = time.perf_counter()
    _logger.debug(f"process_time (sec): {e_pt - s_pt}")
    _logger.debug(f"perf_counter (sec): {e_pc - s_pc}")

    # print(df)

    return df


# def _agnostic_to_utc(time_in, localzone):
#     """A simple converter, local timezone-agnostic to UTC."""
#     return tz(localzone).localize(time_in).astimezone(tz("UTC"))
