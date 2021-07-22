import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


@pytest.fixture
def project():
    from core import project

    return project.Project()


def test_get(project):
    from core import utils
    from core.project import Project

    __directory = utils.Directory()
    assert project.get_path()[utils.FROM] \
           == utils.ROOT + __directory.get_from(Project.HLAB)


def test_set(project):
    project.set_path()
