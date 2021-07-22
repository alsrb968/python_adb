import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


@pytest.fixture
def project():
    from core import project

    return project.Project()


def test_get_path(project):
    from core import utils
    from core.project import Project

    __directory = utils.Directory()
    assert project.get_path()[utils.FROM] \
           == utils.ROOT + __directory.get_from(Project.HLAB)


def test_set_path(project):
    _proj = project.HLAB
    project.set_path(_proj)
    assert project.get_project() == _proj


def test_cwd():
    from core import log
    from pathlib import Path

    log.i(os.getcwd())
    log.i(os.path.realpath(__file__))
    p = Path(os.path.realpath(__file__))
    log.i(str(p.parent.parent))
