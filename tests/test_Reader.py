# -*- coding: utf-8 -*-

import pytest

from speedtest_reader import Reader
from speedtest_reader.util import ValidationException

import helpers

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"


def test_Reader():

    # Initialization

    # invalid source type
    with pytest.raises(ValidationException) as e:
        Reader(None)
    assert "Cannot read" in e.value.message

    # file nonexistent
    with pytest.raises(ValidationException):
        Reader("/inexistent")
    assert "Cannot read" in e.value.message

    # binary
    with pytest.raises(ValidationException):
        Reader(helpers.binfile)
    assert "Cannot read" in e.value.message
    helpers.binfile.seek(0)

    # TODO Add testcases around keyword arg 'cols'.

    # type of 'cols' not `str` or `list`
    # "all"
    # `str` other than "all"
    # value not in columns available
    # value more than once
    #

    # TODO Add testcases for 'copy_df'.

    # start > end
    # start == end
    # start before earliest, end after latest ts
    # all of start is [not] None, end is [not] None combined
    # Use tslocal-decorator to verify time deltas between EST-UTC, UTC-Zurich
    # start is bogus, end is bogus
    #
