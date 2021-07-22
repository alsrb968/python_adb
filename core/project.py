import json
import os
from collections import OrderedDict


class Project:
    BENZ_SB = 'benz_sb'
    BENZ_SG = 'benz_sg'
    KA4 = 'ka4'
    SCANIA = 'scania'
    DPECO = 'dpeco'
    HLAB = 'hlab'

    __json = OrderedDict()
    __JSON_FILE = '{}/PycharmProjects/python_adb/path.json'.format(os.getenv('HOME'))

    def __init__(self):
        self.get_path()

    def get_path(self):
        from core import utils, log

        if os.path.exists(self.__JSON_FILE) is False \
                or os.path.getsize(self.__JSON_FILE) < 10:
            self.set_path(Project.HLAB)
            log.w('setting project default HLAB')

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
        self.__json[utils.PORT] = __port.get_port(_project)

        with open(self.__JSON_FILE, 'w') as outfile:
            json.dump(self.__json, outfile, ensure_ascii=False, indent='\t')

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