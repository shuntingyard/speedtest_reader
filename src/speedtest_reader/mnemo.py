# -*- coding: utf-8 -*-
"""
TODO Lorem ipsum sit blah...
                     blah...

Note: This skeleton file can be safely removed if not needed!
"""

import _io
import logging
import os

from datetime import datetime
from pytz import timezone

import dateparser
import tzlocal

from pkg_resources import get_distribution, DistributionNotFound

from speedtest_reader import reader

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"


def _read_by_mnemonic(source, mnemonic, tz=None):
    # Return:
    #   pandas DataFrame,
    #   start_timestamp (UTC),
    #   end_timestamp (UTC) (both datetime)

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

        return _read_by_ts(source, start=start, end=end, tz=tz)
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
