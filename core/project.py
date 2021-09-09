import json
import os
from collections import OrderedDict
from pathlib import Path
from core import utils, log


class Project:
    __JSON_FILE = '{0}/path.json'.format(Path(os.path.dirname(os.path.realpath(__file__))).parent)
    __default_name = utils.ProjectNames.HLAB

    __root: str = utils.ROOT
    __name: str = None
    __from: str = None
    __to: str = None
    __port: str = None
    __version: str = None

    def __init__(self, name: str = None):
        if name:
            self.save_json(name)
        else:
            self.load_json()

    def load_json(self):
        __json: dict = OrderedDict()
        if os.path.exists(self.__JSON_FILE) is False \
                or os.path.getsize(self.__JSON_FILE) < 10:
            self.save_json(self.__default_name)
            log.w('create %s' % self.__JSON_FILE)
            log.w('set project default %s' % self.__default_name)
            return

        with open(self.__JSON_FILE, 'r') as infile:
            __json = json.load(infile)

        for key in __json.keys():
            if key == utils.JsonKeys.ROOT:
                self.__root = __json[utils.JsonKeys.ROOT]
            elif key == utils.JsonKeys.NAME:
                self.__name = __json[utils.JsonKeys.NAME]
            elif key == utils.JsonKeys.FROM:
                self.__from = __json[utils.JsonKeys.FROM]
            elif key == utils.JsonKeys.TO:
                self.__to = __json[utils.JsonKeys.TO]
            elif key == utils.JsonKeys.PORT:
                self.__port = __json[utils.JsonKeys.PORT]
            elif key == utils.JsonKeys.VERSION:
                self.__version = __json[utils.JsonKeys.VERSION]

        if not self.__name \
                or not self.__from \
                or not self.__to \
                or not self.__port \
                or not self.__version:
            self.save_json(self.__default_name)
            log.w('set project default %s' % self.__default_name)

    def save_json(self, name=None):
        __json: dict = OrderedDict()
        self.__root = utils.ROOT
        if name:
            self.__name = name
            self.__from = utils.PROJECT_FROM_DIR.get(name)
            self.__to = utils.PROJECT_TO_DIR.get(name)
            self.__port = utils.PROJECT_PORT.get(name)
            self.__version = utils.PROJECT_VERSION.get(name)
            log.w('project set %s' % name)

        if not self.__name \
                or not self.__from \
                or not self.__to \
                or not self.__port \
                or not self.__version:
            self.__name = self.__default_name
            self.__from = utils.PROJECT_FROM_DIR.get(self.__default_name)
            self.__to = utils.PROJECT_TO_DIR.get(self.__default_name)
            self.__port = utils.PROJECT_PORT.get(self.__default_name)
            self.__version = utils.PROJECT_VERSION.get(self.__default_name)
            log.w('project set default %s' % self.__default_name)

        __json[utils.JsonKeys.ROOT] = self.__root
        __json[utils.JsonKeys.NAME] = self.__name
        __json[utils.JsonKeys.FROM] = self.__from
        __json[utils.JsonKeys.TO] = self.__to
        __json[utils.JsonKeys.PORT] = self.__port
        __json[utils.JsonKeys.VERSION] = self.__version

        with open(self.__JSON_FILE, 'w') as outfile:
            json.dump(__json, outfile, ensure_ascii=False, indent='\t')

        log.d('save project name = %s' % self.__name)

    def get_root(self):
        return self.__root

    def get_name(self):
        return self.__name

    def get_from(self):
        return self.__from

    def get_to(self):
        return self.__to

    def get_port(self):
        return self.__port

    def get_version(self):
        return self.__version

    def get_packages(self):
        return utils.PROJECT_PACKAGE_NAME.get(self.get_name())

    def to_string(self):
        return 'root={_root}, name={_name}, from={_from}, to={_to}, port={_port}, version={_version}'\
            .format(_root=self.__root,
                    _name=self.__name,
                    _from=self.__from,
                    _to=self.__to,
                    _port=self.__port,
                    _version=self.__version)
