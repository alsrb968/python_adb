import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


@pytest.fixture
def adb():
    from core.adb import Adb
    from core.project import Project

    return Adb(Project())


def test_remount(adb):
    assert adb.remount() == 'remount succeeded'


def test_launch(adb):
    assert ('bash arg: hanhwa.lm18i.launcher' in adb.app_launch('hanhwa.lm18i.launcher')) is True


def test_capture(adb):
    path = adb.screen_capture()
    print('path = {}'.format(path))
    print('exist = {}'.format(os.path.exists(path)))
    assert os.path.exists(path) is True


def test_key_event(adb):
    assert adb.key_event('HOME') is 0


def test_version_name(adb):
    assert adb.version_name('com.polstar.polnav6') == 'versionName=134641C V.6383'


def test_broadcast(adb):
    assert ('Broadcast completed: result=0' in adb.broadcast('com.litbig.action.BOOT_COMPLETED')) is True
