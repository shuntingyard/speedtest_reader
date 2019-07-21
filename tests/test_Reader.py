# -*- coding: utf-8 -*-

import pytest

from speedtest_reader import Reader
from speedtest_reader import ValidationException

from . import helpers

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"


def test_Reader():
    # invalid source type
    with pytest.raises(ValidationException) as e:
        Reader(None)
    assert "Invalid source type:" in e.value.message

    # file nonexistent
    with pytest.raises(FileNotFoundError):
        Reader("./testdata/bogus.csv")

    # # file access denied
    # with pytest.raises(OSError) as e:
    #     read_by_ts("./testdata/inaccessible.csv")
    # assert str(e.value) == "Initializing from file failed"

    # # file with strange input
    # with pytest.raises(UnicodeDecodeError):
    #     read_by_ts("./testdata/random.file")

    # TODO Remove this! Then add some test for copy_df, e.g.
    #
    # start > end
    # start == end
    # start before earliest, end after latest ts
    # all of start is [not] None, end is [not] None combined
    # Use tslocal-decorator to verify time deltas between EST-UTC, UTC-Zurich
    # start is bogus, end is bogus
    # 
