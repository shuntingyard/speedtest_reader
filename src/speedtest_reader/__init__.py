# -*- coding: utf-8 -*-

"""
TODO
"""

import logging

import pandas as pd

from pkg_resources import get_distribution, DistributionNotFound

from speedtest_reader import util

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

# globals __version__
try:
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

# globals other
logger = logging.getLogger(__name__)


class Reader:
    """
    Keep DataFrame in memory and append to it when read requests come in.

    Attributes:
        source      file-like, as produced by `speedtest-cli --csv`
        cols        `list` columns to read into the DataFrame, default is
                    `['Download', 'Upload']`, Timestamp is always read.
    """
    CHUNKSIZE = 10000

    def __init__(self, source, cols=None):

        self._infile = source
        if not cols:
            self._cols = ["Download", "Upload"]
        else:
            self._cols = cols
        if "Timestamp" not in self._cols:
            self._cols.append("Timestamp")
            self._drop_ts = True
        else:
            self._drop_ts = False

        self._row_count = 0
        self._ramdf = pd.DataFrame()

        # eager initialisation
        self._status = "INIT"
        self._ramdf = self.copy_df(None, None)
        self._status = "READ"

    @util.stopwatch
    def copy_df(self, start, end):
        """
        Get a copy of the `pandas.DataFrame` in memory, limited by:

        Args:
            start   `datetime`: UTC used for lower bound of copy
            end     `datetime`: UTC used for upper bound of copy

        Return:
            `pandas.DataFrame`
        """
        len_before = len(self._ramdf.index)

        for chunk in pd.read_csv(
            self._infile,
            chunksize=Reader.CHUNKSIZE,
            skiprows=range(1, len(self._ramdf.index) + 1),
            engine="c",
            usecols=self._cols,
        ):
            # create column to be used for slicing
            chunk["ts"] = [
                pd.to_datetime(ts, utc=True) for ts in chunk["Timestamp"]
            ]
            chunk.set_index("ts", inplace=True)

            # Append to DataFrame in memory
            self._ramdf = self._ramdf.append(chunk, sort=False)

        # remove if not on demand
        if self._drop_ts:
            self._ramdf.drop("Timestamp", axis=1, inplace=True)

        # end of read loop
        logger.info(
            "on {} df totals {} and grew by {}".format(
                self._status,
                len(self._ramdf.index),
                len(self._ramdf.index) - len_before,
            )
        )

        # Find index values for slicing.
        lower = self._ramdf.index.searchsorted(start)
        upper = self._ramdf.index.searchsorted(end)

        # Slice according to values.
        df = self._ramdf
        if start:
            if end:
                df = df.iloc[lower:upper]
            else:
                df = df.iloc[lower:]
        else:
            if end:
                df = df.iloc[:upper]

        return df.copy()


@util.stopwatch
def format_timestamps(start=None, end=None, tz=None):
    """
    Format args for `Reader.copy_df`.

    Args:
        start_time  `str`, `datetime`, `None`: 'from' timestamp
        end_time    `str`, `datetime`, `None`: 'to'   timestamp
        tz          `str`: timezone used for slicing, if `None`, module
                    tzlocal is used.

    Return:
        `datetime`: start, `datetime`: end
    """
    # check start
    if start:
        if isinstance(start, str):
            start = util.parse_ts(start)
            # logger.debug("start, post parsing: %s" % start)

        start = util.datetime_to_utc(start, tz)
        # logger.debug("start, post conversion: %s" % start)

    # check end
    if end:
        if isinstance(end, str):
            end = util.parse_ts(end)
            # logger.debug("end, post parsing: %s" % end)

        end = util.datetime_to_utc(end, tz)
        # logger.debug("end, post conversion: %s" % end)

    return start, end
