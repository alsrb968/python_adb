#!/usr/bin/python

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def test_proj():
    from core import utils, adb

    assert adb.JSON_KEYS.proj('benz_sb') == utils.DIR_FROM.SMARTMONITOR