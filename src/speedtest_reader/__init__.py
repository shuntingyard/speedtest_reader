# -*- coding: utf-8 -*-
"""
TODO Lorem ipsum sit blah...
                     blah...

Note: This skeleton file can be safely removed if not needed!
"""

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

import _io
import os

from datetime import datetime
from pytz import timezone

import dateparser
import tzlocal

from pkg_resources import get_distribution, DistributionNotFound

from speedtest_reader.slicer import slice_input

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound


class ValidationException(Exception):
    """A unifying wrapper around what's bad behind the scene.

    Attributes:
        parent - the exception one step back in the trace
        message - explanation of the error
    """

    def __init__(self, parent, message):
        self.parent = parent
        self.message = message


def read_by_ts(source, start=None, end=None, tz=None):
    """Read by timestamp(s):
        On str input module dateparser is used.
        Datetime values are converted to UTC.
        None returns all data in infile.

        Args:
            source      the data source (str, bytes or os.PathLike object)
            start_time  timezone-agnostic start value (str, datetime, None)
            end_time    timezone-agnostic end value   (str, datetime, None)
            tz          timezone (str), if None module tzlocal is used.

        Return:
            pandas DataFrame,
            start_timestamp (UTC),
            end_timestamp (UTC) (both datetime)
    """
    # check allowed types to convey input data
    if type(source) in [str, os.PathLike, _io.StringIO]:
        pass
    else:
        raise ValidationException(None, "Invalid source type: %s" % source)

    # check start
    if start:
        if isinstance(start, str):
            start = _parse(start)
            print("start, post parsing:", start)

        start = _datetime_to_utc(start, tz)
        print("start, post conversion")

    # check end
    if end:
        if isinstance(end, str):
            end = _parse(end)
            print("end, post parsing:", start)

        end = _datetime_to_utc(end, tz)
        print("end, post conversion")

    return slice_input(source, start, end), start, end


def _parse(ts):
    # Parse a timestamp (from str).
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


def _datetime_to_utc(time_in, tz):
    # Convert time_in to UTC.

    if not (
        time_in.tzinfo is None or time_in.tzinfo.utcoffset(time_in) is None
    ):
        # preserve tzinfo if it is there
        pass
    else:
        if tz:
            # if we get one from user, use tz to localize
            time_in = timezone(tz).localize(time_in)
        else:
            # if noting else use the local timezone
            time_in = tzlocal.get_localzone().localize(time_in)

    return time_in.astimezone(timezone("UTC"))


def read_by_mnemonic(source, mnemonic, tz=None):
    """Deprecated - this is covered in a much more flexible way
    by module dateparser.
    """
    if mnemonic in get_mnemonics():
        # helper variables
        last_midnight = datetime.combine(datetime.now(), datetime.min.time())

        if mnemonic == "from_midnight":
            start = last_midnight
        elif mnemonic == "from_1st_of_month":
            start = last_midnight.replace(day=1)
        else:
            start = None

        # In all cases so far end is `None` (i.e. the present).
        end = None

        return read_by_ts(source, start=start, end=end, tz=tz)
    else:
        raise ValidationException(None, "Not a mnemonic: %s" % mnemonic)


def get_mnemonics():
    """Deprecated, see above. Return all mnemonics for time frames..."""
    return [
        # "last24hours",
        # "last7days",
        # "last30days",
        "from_midnight",
        # "from_sunday",
        # "from_monday",
        "from_1st_of_month",
        # "from_jan_1st",
        "all",
    ]
