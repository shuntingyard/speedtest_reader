# -*- coding: utf-8 -*-

import logging

from io import StringIO

import pytest
import tzlocal

from datetime import datetime
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError

from speedtest_reader import get_mnemonics
from speedtest_reader import read_by_mnemonic
from speedtest_reader import read_by_ts
from speedtest_reader import ValidationException

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

# helpers for testing
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

# TODO remedy required: this is usable ONE time, then its position is at EOF.
infile = StringIO(CSV)

infile = "./testdata/headers+1.csv"

midnight = tzlocal.get_localzone().localize(
    datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
)  # last midnight with tester's timezone

my_offset = midnight.utcoffset()  # tester's offset from UTC

logging.basicConfig(level=30)  # WARN: 30, INFO: 20, DEBUG: 10
# end helpers


def test_read_by_mnemonic():
    # unknown mnemonic test
    with pytest.raises(ValidationException) as e:
        read_by_mnemonic(infile, "bogus")
    assert "Not a mnemonic:" in e.value.message

    # verify timestamp correctness
    for shorthand in get_mnemonics():

        _, start, _ = read_by_mnemonic(infile, shorthand)
        if shorthand == "from_midnight":
            assert start == midnight
        elif shorthand == "from_1st_of_month":
            assert start == midnight.replace(day=1)
        else:
            assert not start


def test_read_by_ts():
    # invalid source type
    with pytest.raises(ValidationException) as e:
        read_by_ts(None)
    assert "Invalid source type:" in e.value.message

    # file nonexistent
    with pytest.raises(FileNotFoundError):
        read_by_ts("./testdata/bogus.csv")

    # file access denied
    with pytest.raises(OSError) as e:
        read_by_ts("./testdata/inaccessible.csv")
    assert str(e.value) == "Initializing from file failed"

    # # file with strange input
    # with pytest.raises(UnicodeDecodeError):
    #     read_by_ts("./testdata/random.file")

    # backend store re-init if source != previous source
    #
    # Read a big file, then read a small one.
    df1, _, _ = read_by_ts("./testdata/guam.csv")
    df2, _, _ = read_by_ts(infile)
    assert len(df1.index) > len(df2.index)

    # bad ts format tests
    with pytest.raises(ValidationException) as e:
        read_by_ts(infile, start="Nat")
    assert "Not converted to datetime:" in e.value.message

    with pytest.raises(ValidationException) as e:
        read_by_ts(infile, end="Bat")
    assert "Not converted to datetime:" in e.value.message

    # Basic time testing -> conversion to UTC using:

    # - naive: our dt must be same as returned value (without tz) + offset.
    dt = midnight.replace(tzinfo=None)
    _, start, _ = read_by_ts(infile, start=dt)
    assert my_offset + start.replace(tzinfo=None) == dt

    dt = midnight.replace(hour=6, minute=30, tzinfo=None)
    _, _, end = read_by_ts(infile, end=dt)
    assert my_offset + end.replace(tzinfo=None) == dt

    # - tz=invalid
    dt = midnight.replace(tzinfo=None)
    with pytest.raises(UnknownTimeZoneError):
        read_by_ts(infile, start=dt, tz="Europe/Rennes")

    # - datetime with (some other) tz info: must NOT be overwritten by our
    #   API implementation!
    dt = midnight.replace(tzinfo=timezone("EST"))
    other_offset = dt.utcoffset()
    _, _, end = read_by_ts(infile, end=dt)
    print(dt, end)
    assert other_offset + end.replace(tzinfo=None) == dt.replace(tzinfo=None)

    #
    # TODO all kind of ts range tests
    #
