#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Command line utility for manual testing
"""

import argparse
import logging
import sys

import pandas as pd

from speedtest_reader import __version__

from speedtest_reader.oldinit import get_mnemonics
from speedtest_reader.oldinit import read_by_mnemonic

from speedtest_reader import format_timestamps
from speedtest_reader import Reader
from speedtest_reader.util import ValidationException

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"


def parse_args(args):
    """Parse command line parameters"""

    parser = argparse.ArgumentParser(
        description="Test utility for the command line",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="speedtest_reader %s" % __version__,
    )
    parser.add_argument(
        dest="infile", help="the file to read from", metavar="infile"
    )
    parser.add_argument(
        "-s", "--start", help="set start timestamp", action="store"
    )
    parser.add_argument(
        "-e", "--end", help="set end timestamp", action="store"
    )
    parser.add_argument(
        "-m",
        "--mnemonic",
        help="set one of %s" % get_mnemonics(),
        action="store",
    )
    parser.add_argument(
        "-Z", "--tz", help="set timezone for slicing", action="store"
    )
    parser.add_argument(
        "-r", type=int, help="set number of DataFrame rows to print", default=5
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        type=int,
        help="set log level (steps of 10, lower is more)",
        default=20,
    )
    return parser.parse_args(args)


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    print(args)
    timezone = args.tz

    # extent of details to print
    logging.basicConfig(level=args.loglevel)
    pd.options.display.max_rows = args.r

    # set up sensor
    sensor1 = Reader(args.infile)

    def slice_s1(**kwargs):
        kwargs["tz"] = timezone
        start, end = format_timestamps(**kwargs)
        return sensor1.copy_df(start, end)

    try:
        if args.mnemonic:
            df = read_by_mnemonic(
                args.infile, args.mnemonic, slicer_tz=args.tz
            )
        else:
            df = slice_s1(start=args.start, end=args.end)

        print(df)

    except ValidationException as e:
        print(e.parent)
        print(e.message)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
