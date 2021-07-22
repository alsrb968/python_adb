import json
from collections import OrderedDict


class Project:
    BENZ_SB = 'benz_sb'
    BENZ_SG = 'benz_sg'
    KA4 = 'ka4'
    SCANIA = 'scania'
    DPECO = 'dpeco'
    HLAB = 'hlab'

    __project = None
    __json = OrderedDict()
    __JSON_FILE = '/Users/minkyu/OneDrive/Litbig/util/python/adb/path.json'

    def __init__(self, project=None):
        self.__project = project

    def get_path(self):
        import utils

        with open(self.__JSON_FILE, 'r') as infile:
            self.__json = json.load(infile)

        if self.__json[utils.FROM]:
            self.__json[utils.FROM] = utils.ROOT + self.__json[utils.FROM]

        return self.__json

    def set_path(self):
        import log
        import utils
        from utils import Directory, Port

        __directory = Directory()
        __port = Port()

        if self.__project is None:
            log.w('project is none')
            exit(-1)

        self.__json[utils.FROM] = __directory.get_from(self.__project)
        self.__json[utils.TO] = __directory.get_to(self.__project)
        self.__json[utils.PORT] = __port.get_port(self.__project)

        with open(self.__JSON_FILE, 'w') as outfile:
            json.dump(self.__json, outfile, ensure_ascii=False, indent='\t')

    def get_project(self):
        return self.__project
