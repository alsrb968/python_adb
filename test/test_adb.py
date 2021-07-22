import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


@pytest.fixture
def adb():
    from core.adb import Adb
    from core.project import Project

    return Adb(Project())


def test_capture(adb):
    path = adb.screen_capture()
    print('path = {}'.format(path))
    print('exist = {}'.format(os.path.exists(path)))
    assert os.path.exists(path) is True


def test_exist():
    path = '{0}/Downloads/1.jpg'.format(os.getenv('HOME'))
    assert os.path.exists(path) is True
