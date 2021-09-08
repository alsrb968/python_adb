import json
import os
from collections import OrderedDict
from pathlib import Path


class Project:
    BENZ_SB = 'benz_sb'
    BENZ_SG = 'benz_sg'
    KA4 = 'ka4'
    SCANIA = 'scania'
    DPECO = 'dpeco'
    HLAB = 'hlab'

    __PACKAGES = {
        BENZ_SB: {},
        BENZ_SG: {},
        KA4: {},
        SCANIA: {},
        DPECO: {},
        HLAB: {'allapps': 'com.android.allapps',
               'settings': 'com.android.settings',
               'documents': 'com.android.documentsui',
               'polnav': 'com.polstar.polnav6',
               'launcher': 'hanhwa.lm18i.launcher'},
    }

    __json = OrderedDict()
    __JSON_FILE = '{0}/path.json'.format(Path(os.path.dirname(os.path.realpath(__file__))).parent)

    def __init__(self):
        self.get_path()

    def get_path(self):
        from core import utils, log

        if os.path.exists(self.__JSON_FILE) is False \
                or os.path.getsize(self.__JSON_FILE) < 10:
            self.set_path(Project.HLAB)
            log.w('create {}'.format(self.__JSON_FILE))
            log.w('set project default {}'.format(self.HLAB))

        with open(self.__JSON_FILE, 'r') as infile:
            self.__json = json.load(infile)

        if self.__json[utils.FROM]:
            self.__json[utils.FROM] = utils.ROOT + self.__json[utils.FROM]

        return self.__json

    def set_path(self, _project):
        from core import log, utils
        from core.utils import Directory, Port

        __directory = Directory()
        __port = Port()

        if _project is None or len(_project) == 0:
            log.w('project is none')
            return

        self.__json[utils.PROJECT] = _project
        self.__json[utils.FROM] = __directory.get_from(_project)
        self.__json[utils.TO] = __directory.get_to(_project)
        self.__json[utils.PORT] = __port.get(_project)

        with open(self.__JSON_FILE, 'w') as outfile:
            json.dump(self.__json, outfile, ensure_ascii=False, indent='\t')

        log.d('set path = {}'.format(_project))

    def get_project(self):
        from core import utils

        return self.__json[utils.PROJECT]

    def get_from(self):
        from core import utils

        return self.__json[utils.FROM]

    def get_to(self):
        from core import utils

        return self.__json[utils.TO]

    def get_port(self):
        from core import utils

        return self.__json[utils.PORT]

    def get_packages(self):
        return self.__PACKAGES.get(self.get_project())

    def get_version(self):
        from core import utils

        __version = utils.Version()
        return __version.get(self.get_project())
