# -*- coding: utf-8 -*-

import logging

from io import StringIO

import pandas as pd
import tzlocal

from datetime import datetime

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

CSV = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n%s\n" % (
    "Server ID",
    "Sponsor",
    "Server Name",
    "Timestamp",
    "Distance",
    "Ping",
    "Download",
    "Upload",
    "Share",
    "IP Address",
    "1234,bkw,Bern,2019-06-16T21:31:30.879143Z,7.3,16.1,10.0,34.7,,1.1.1.1",
)

# TODO remedy required: this is usable ONE time, then its position is at EOF.
infile = StringIO(CSV)

infile = "./testdata/headers+1.csv"

midnight = tzlocal.get_localzone().localize(
    datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
)  # last midnight with tester's timezone

my_offset = midnight.utcoffset()  # tester's offset from UTC

logging.basicConfig(level=30)  # WARN: 30, INFO: 20, DEBUG: 10


def miniframe(ts):
    """Returns a minimal DataFrame with one row.
    Args:
        ts  (str) timestamp to convert to the index value
    """
    df = pd.DataFrame(columns=["ts", "naught"])
    df.loc[0] = [ts, None]
    df["ts"] = [pd.to_datetime(ts) for ts in df["ts"]]
    df.set_index("ts", inplace=True)
    return df
