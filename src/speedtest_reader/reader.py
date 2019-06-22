# -*- coding: utf-8 -*-

"""Parse file(s) written by 'speedtest-cli' into pandas DataFrame(s).
"""
import logging
import time

# import matplotlib.dates as mdates
import pandas as pd

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def _slice_input(source, start, end, cols=None):
    """Slice input df using start and end."""

    # ACCCESS DATAFRAME
    df = Reader(source, cols=cols)._get_df()

    s_pt = time.process_time()
    s_pc = time.perf_counter()

    # _logger.debug(f"{start} is lower bound of slice")
    # _logger.debug(f"{end} is upper bound of slice")

    # Find index values for slicing.
    lower = df.index.searchsorted(start)
    upper = df.index.searchsorted(end)

    # Slice according to values.
    if start:
        if end:
            df = df.iloc[lower:upper]
        else:
            df = df.iloc[lower:]
    else:
        if end:
            df = df.iloc[:upper]
        else:
            pass

    # _logger.debug(f"{df.index.min()} is min index in DataFrame")
    # _logger.debug(f"{df.index.max()} is max index in DataFrame")

    e_pt = time.process_time()
    e_pc = time.perf_counter()
    _logger.debug(f"process_time (sec): {e_pt - s_pt}")
    _logger.debug(f"perf_counter (sec): {e_pc - s_pc}")

    # print(df)

    return df


# don't bear the burden of singletons ;)
class MonostatePattern:

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Reader(MonostatePattern):
    """Keep DataFrame in memory and append to it when read requests
    come in.

    Attributes:
        source      file-like, as produced by `speedtest-cli --csv`
                        -> impl: create new ram structure on change!
        cols        ...
                        -> impl: [if need be] re-read source on change!
    """

    CHUNKSIZE = 1000

    def __init__(self, source, cols=None):

        # idiom for all versions of Python:
        super(Reader, self).__init__()

        # conditional init:
        if (
            len(self.__dict__) > 0
            and self._infile == source
            and self._cols == cols
        ):
            pass  # monostate existed, infile same as before

        else:
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
            self._ramdf = self._get_df()
            self._status = "READ"

    def _get_df(self):

        len_before = len(self._ramdf.index)

        s_pt = time.process_time()
        s_pc = time.perf_counter()

        for chunk in pd.read_csv(
            self._infile,
            chunksize=Reader.CHUNKSIZE,
            skiprows=range(1, len(self._ramdf.index) + 1),
            engine="c",
            usecols=self._cols,
            converters={
                # TODO to decorators!
                # "Timestamp": lambda t: pd.to_datetime(t),
                # "Download": lambda d: float(d) / (10 ** 6),
                # "Upload": lambda u: float(u) / (10 ** 6),
            },
        ):
            # create column to be used for slicing
            chunk["ts_datetime"] = [
                pd.to_datetime(ts, utc=True) for ts in chunk["Timestamp"]
            ]
            chunk.set_index("ts_datetime", inplace=True)

            # # Add matplotlib-friendly timestamp.TODO to decorators!
            # if self._mpl_ts:
            #     chunk["mtimestamp"] = [
            #         mdates.date2num(ts) for ts in chunk["Timestamp"]
            #     ]

            # # Add timezone-agnostic timestamp.TODO to decorators!

            # if self._agnostic:  # What a name - the two combined :)
            #     chunk["agnostic_t"] = [
            #         ts.replace(tzinfo=None) for ts in chunk["Timestamp"]
            #     ]

            # Append to DataFrame in memory
            self._ramdf = self._ramdf.append(chunk, sort=False)

        # remove if not on demand
        if self._drop_ts:
            self._ramdf.drop("Timestamp", axis=1, inplace=True)

        # end of read loop
        e_pt = time.process_time()
        e_pc = time.perf_counter()
        _logger.debug(f"process_time (sec): {e_pt - s_pt}")
        _logger.debug(f"perf_counter (sec): {e_pc - s_pc}")

        _logger.info(
            "{}: df totals {} and grew by {}".format(
                self._status,
                len(self._ramdf.index),
                len(self._ramdf.index) - len_before,
            )
        )

        return self._ramdf.copy()
