# -*- coding: utf-8 -*-

"""
Utility functions, classes and API decorators
"""

import functools
import time

from datetime import datetime
from matplotlib import dates as mdates
from pytz import timezone

import dateparser
import tzlocal

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"


def stopwatch(fn):
    """
    Log (INFO) how much time is spent in decorated fn.
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        end = time.perf_counter()
        msec = (end - start) * 1000
        # log results
        logger = fn.__globals__.get("logger", None)
        if logger:
            logger.info(
                "{elapsed:4d} msec elapsed in '{name}'".format(
                    elapsed=int(round(msec, 1)), name=fn.__qualname__
                )
            )
        return result

    return wrapper


def parse_ts(ts):
    """
    Wrap `dateparser` to validate parsing results.
    """
    try:
        ts_out = dateparser.parse(ts)
        if not isinstance(ts_out, datetime):
            raise ValidationException(
                None, "Not converted to datetime: %s" % ts
            )
        return ts_out
    # According to doc, this is the only one raised by dateparser.parse!
    except ValueError as e:
        raise ValidationException(e, "Date parsing failed.")


def datetime_to_utc(dt, tz):
    """
    Convert `dt` to UTC.

    If `dt` is not timezone-agnostic return as timezone UTC.

    If `dt` is timezone-agnostic:
        use `tz` for localization if present or else
        use module `tzlocal`,
        then return as timezone UTC
    """
    if not (
        dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None
    ):
        # preserve tzinfo if it is there
        pass
    else:
        if tz:
            # If we get one from user, use tz to localize.
            dt = timezone(tz).localize(dt)
        else:
            # if noting else: local timezone
            dt = tzlocal.get_localzone().localize(dt)

    return dt.astimezone(timezone("UTC"))


class ValidationException(Exception):
    """
    A unifying wrapper around what's bad behind the scenes.

    Attributes:
        parent - the exception one step back in the trace
        message - explanation of the error
    """

    def __init__(self, parent, message):
        self.parent = parent
        self.message = message


def to_Mbit(fn):
    """
    Decorator: convert bit to Mbit in download and upload columns.
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        df = fn(*args, **kwargs)
        df["Download"] = [f / 10 ** 6 for f in df["Download"]]
        df["Upload"] = [f / 10 ** 6 for f in df["Upload"]]
        return df

    return wrapper


def append_mpldate(colname="mpldate"):
    """
    Decorator: append timestamp column suitable for matplotlib
    (matplotlib.dates).

    Args:
        colname     `str`: column name to use (default 'mpldate')
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            df = fn(*args, **kwargs)
            df[colname] = [mdates.date2num(ts) for ts in df.index]
            return df

        return wrapper

    return decorator


def append_tslocal(colname="tslocal", tz=None):
    """
    Decorator: append localized timestamp column -
    suitable for plotly, dash etc.

    Args:
        colname     `str`: column name to use (default 'mpldate')
        tz          `str`: explicitly set local zone to use
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            df = fn(*args, **kwargs)
            # Requires pandas >= 0.15.0 to get rid of tz.
            if tz:
                df[colname] = [
                    ts.astimezone(timezone(tz)).tz_localize(None)
                    for ts in df.index
                ]
            else:
                df[colname] = [
                    ts.astimezone(tzlocal.get_localzone()).tz_localize(None)
                    for ts in df.index
                ]
            return df

        return wrapper

    return decorator
