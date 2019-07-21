# -*- coding: utf-8 -*-

import pytest

from speedtest_reader import get_mnemonics
from speedtest_reader import _read_by_mnemonic as dt_mnemonic
from speedtest_reader import read_by_mnemonic
from speedtest_reader import ValidationException

from . import helpers

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"


def test_read_by_mnemonic():
    # unknown mnemonic test
    with pytest.raises(ValidationException) as e:
        read_by_mnemonic(helpers.infile, "bogus")
    assert "Not a mnemonic:" in e.value.message

    # verify timestamp correctness
    for shorthand in get_mnemonics():

        _, start, _ = dt_mnemonic(helpers.infile, shorthand)
        if shorthand == "from_midnight":
            assert start == helpers.midnight
        elif shorthand == "from_1st_of_month":
            assert start == helpers.midnight.replace(day=1)
        else:
            assert not start
