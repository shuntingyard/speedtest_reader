# -*- coding: utf-8 -*-
"""
The core for parsing file(s) written by 'speedtest-cli' into pandas
DataFrame(s).

Decorators are exposed in this module.
"""
import logging
import time

# import functools
import matplotlib.dates as mdates
import pandas as pd
import tzlocal

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

logger = logging.getLogger(__name__)


def bit_to_Mbit(func):
    """Decorator: convert bit to Mbit in upload and download columns."""

    def decorated(*args, **kwargs):
        df = func(*args, **kwargs)
        df["Download"] = [f / 10 ** 6 for f in df["Download"]]
        df["Upload"] = [f / 10 ** 6 for f in df["Upload"]]
        return df

    return decorated


def append_mdates(colname="mpldate"):
    """Decorator: append timestamps suitable for matplotlib
    (matplotlib.dates)."""

    def decorator(func):
        def decorated(*args, **kwargs):
            # do_something(*outer_args,**outer_kwargs)
            df = func(*args, **kwargs)
            df[colname] = [mdates.date2num(ts) for ts in df.index]
            return df

        return decorated

    return decorator


def append_tslocal(colname="tslocal"):
    """Decorator: append localized timestamps suitable for plotly, dash etc."""

    def decorator(func):
        def decorated(*args, **kwargs):
            # do_something(*outer_args,**outer_kwargs)
            df = func(*args, **kwargs)

            # Requires pandas >= 0.15.0 to get rid of tz.
            df[colname] = [
                ts.astimezone(tzlocal.get_localzone()).tz_localize(None)
                for ts in df.index
            ]
            return df

        return decorated

    return decorator


