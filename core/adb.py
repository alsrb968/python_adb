import os
import time
from collections import OrderedDict


class Adb:
    from core.project import Project

    __project = None
    __json = OrderedDict()

    def __init__(self, _project: Project):
        self.__project = _project
        self.__json = _project.get_path()

    def remount(self):
        os.system('adb remount')

    def reboot(self, _reason=''):
        if len(_reason) > 0:
            os.system('adb reboot {reason}'.format(reason=_reason))
            return
        os.system('adb reboot')

    def push(self, _dir, _target):
        from core import utils

        os.system('adb push {root}{out}{dir}{target} {dir}'
                  .format(root=self.__json.get(utils.FROM),
                          out=self.__json.get(utils.TO),
                          dir=_dir,
                          target=_target))

    def install(self, _dir, _target):
        from core import utils

        os.system('adb install -r {root}{out}{dir}{target}/{target}.apk'
                  .format(root=self.__json.get(utils.FROM),
                          out=self.__json.get(utils.TO),
                          dir=_dir,
                          target=_target))

    def lib_push(self, _target):
        from core import utils

        self.push(utils.LIB_DIR, _target)

    def framework_push(self, _target):
        from core import utils

        self.push(utils.FRAMEWORK_DIR, _target)

    def priv_app_push(self, _target):
        from core import utils

        self.push(utils.PRIV_APP_DIR, _target)

    def app_push(self, _target):
        from core import utils

        self.push(utils.APP_DIR, _target)

    def priv_app_install(self, _target):
        from core import utils

        self.install(utils.PRIV_APP_DIR, _target)

    def app_install(self, _target):
        from core import utils

        self.install(utils.APP_DIR, _target)

    def app_launch(self, _package):
        os.system('adb shell monkey -p {pkg} -c android.intent.category.LAUNCHER 1'
                  .format(pkg=_package))

    def fastboot(self, _image):
        from core import utils
        from core.project import Project

        if _image == 'dtb' and self.__project.get_project() == Project.HLAB:
            os.system('fastboot flash {img} {root}{out}tcc8030-android-lpd4321_sv0.1.dtb'
                      .format(root=self.__json.get(utils.FROM),
                              out=self.__json.get(utils.TO),
                              img=_image))

        else:
            os.system('fastboot flash {img} {root}{out}{img}.img'
                      .format(root=self.__json.get(utils.FROM),
                              out=self.__json.get(utils.TO),
                              img=_image))

    def fastboot_reboot(self):
        os.system('fastboot reboot')

    def screen_capture(self) -> str:
        from core import log

        __format = '%Y%m%d_%H%M%S.png'
        __result = time.strftime(__format, time.localtime())
        os.system('adb shell screencap -p /data/{0}'.format(__result))
        os.system("adb pull /data/{0} {1}/Downloads".format(__result, os.getenv('HOME')))

        out_path = '{0}/Downloads/{1}'.format(os.getenv('HOME'), __result)

        if os.path.exists(out_path) is False:
            log.e('screen capture fail')
            return ''

        log.i("screen capture path = {0}".format(out_path))
        return out_path

    def broadcast(self, _what: str):
        os.system('adb shell am broadcast -a {}'.format(
            {'boot_completed': 'com.litbig.action.BOOT_COMPLETED'}.get(_what)))

    def key_event(self, _what: str):
        os.system('adb shell input keyevent KEYCODE_{}'.format(_what.upper()))

    def version_name(self, _what: str):
        os.system('adb shell dumpsys package {} | grep versionName'.format(
            {'polnav': 'com.polstar.polnav6',
             'launcher': 'hanhwa.lm18i.launcher'}.get(_what)))
