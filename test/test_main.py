import os
import sys
import pytest

import main

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from core.adb import Adb
from core.project import Project


@pytest.fixture
def adb():
    return Adb(Project())


