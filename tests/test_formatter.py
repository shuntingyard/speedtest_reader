# -*- coding: utf-8 -*-

import pytest

from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError

from speedtest_reader import format_timestamps
from speedtest_reader.util import ValidationException

import helpers

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"


def test_format_timestamps():

    # Bad ts format tests

    with pytest.raises(ValidationException) as e:
        format_timestamps(start="Nat")
    assert "Not converted to datetime:" in e.value.message

    with pytest.raises(ValidationException) as e:
        format_timestamps(end="Bat")
    assert "Not converted to datetime:" in e.value.message

    # Basic time testing -> conversion to UTC using:

    # - naive: our dt must be same as returned value (without tz) + offset.
    dt = helpers.midnight.replace(tzinfo=None)
    start, _ = format_timestamps(start=dt)
    assert helpers.my_offset + start.replace(tzinfo=None) == dt

    dt = helpers.midnight.replace(hour=6, minute=30, tzinfo=None)
    _, end = format_timestamps(end=dt)
    assert helpers.my_offset + end.replace(tzinfo=None) == dt

    # - tz=invalid
    dt = helpers.midnight.replace(tzinfo=None)
    with pytest.raises(UnknownTimeZoneError):
        format_timestamps(start=dt, tz="Europe/Rennes")

    # - datetime with (some other) tz info: must NOT be overwritten by our
    #   API implementation!
    dt = helpers.midnight.replace(tzinfo=timezone("EST"))
    other_offset = dt.utcoffset()
    _, end = format_timestamps(end=dt)
    assert other_offset + end.replace(tzinfo=None) == dt.replace(tzinfo=None)
