from __future__ import unicode_literals

from io import StringIO

import pandas as pd

# from speedtest_reader import read_by_ts

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
    "1234,bkw,Bern,2019-06-16T21:31:30.879143Z,7.3,16.1,22.1,34.7,,1.1.1.1",
)

infile = StringIO(CSV)

print(
    pd.read_csv(
        infile,
        engine="c",
        converters={
            "Timestamp": lambda t: pd.to_datetime(t),
            "Download": lambda d: float(d) / (10 ** 6),
            "Upload": lambda u: float(u) / (10 ** 6),
        },
    )
)

print(
    pd.read_csv(
        infile,
        engine="c",
        converters={
            "Timestamp": lambda t: pd.to_datetime(t),
            "Download": lambda d: float(d) / (10 ** 6),
            "Upload": lambda u: float(u) / (10 ** 6),
        },
    )
)
# read_by_ts(infile)

# for line in infile.readline():
#     print(line)
