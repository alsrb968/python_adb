import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from core import utils
from core.project import Project
from core import log
from pathlib import Path
from core.utils import ProjectNames


def test_cwd():
    log.i(os.getcwd())
    log.i(os.path.realpath(__file__))
    p = Path(os.path.realpath(__file__))
    log.i(str(p.parent.parent))


def test_project_constructor():
    names = set()
    names.add(ProjectNames.BENZ_SB)
    names.add(ProjectNames.BENZ_SG)
    names.add(ProjectNames.KA4)
    names.add(ProjectNames.SCANIA)
    names.add(ProjectNames.DPECO)
    names.add(ProjectNames.HLAB)
    for name in names:
        __project = Project(name)
        assert __project.get_name() == name


@pytest.fixture
def project():
    return Project(ProjectNames.HLAB)


def test_load_json(project):
    assert project.get_from() == utils.PROJECT_FROM_DIR.get(ProjectNames.HLAB)


def test_save_json(project):
    __project_name = ProjectNames.HLAB
    _project = Project(name=__project_name)
    project.save_json(_project.get_name())
    assert project.get_name() == __project_name


def test_get_name(project):
    assert project.get_name() == ProjectNames.HLAB


def test_get_from(project):
    assert project.get_from() == utils.PROJECT_FROM_DIR.get(ProjectNames.HLAB)


def test_get_to(project):
    assert project.get_to() == utils.PROJECT_TO_DIR.get(ProjectNames.HLAB)


def test_get_port(project):
    assert project.get_port() == utils.PROJECT_PORT.get(ProjectNames.HLAB)


def test_get_version(project):
    assert project.get_version() == utils.AndroidVersion.P


def test_get_packages(project):
    assert project.get_packages().get('allapps') == utils.PROJECT_PACKAGE_NAME.get(ProjectNames.HLAB).get('allapps')


def test_to_string(project):
    print(project.to_string())
