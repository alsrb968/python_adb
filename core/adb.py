import os
import subprocess
import time
from core.project import Project
from core import utils, log


class Adb:
    __project = None

    def __init__(self, _project: Project):
        self.__project = _project

    def command(self, _cmd: str):
        return subprocess.check_output(_cmd, shell=True).decode('utf-8').strip()

    def remount(self):
        return self.command('adb remount')

    def reboot(self, _reason=''):
        if len(_reason) > 0:
            return os.system('adb reboot {reason}'.format(reason=_reason))

        return os.system('adb reboot')

    def push(self, _dir, _target):
        return os.system('adb push {_root}{_from}{_to}{dir}{target} {dir}'
                         .format(_root=self.__project.get_root(),
                                 _from=self.__project.get_from(),
                                 _to=self.__project.get_to(),
                                 dir=_dir,
                                 target=_target))

    def install(self, _dir, _target):
        return os.system('adb install -r {_root}{_from}{_to}{dir}{target}.apk'
                         .format(_root=self.__project.get_root(),
                                 _from=self.__project.get_from(),
                                 _to=self.__project.get_to(),
                                 dir=_dir,
                                 target=_target))

    def uninstall(self, _package):
        return os.system('adb uninstall {package_name}'
                         .format(package_name=_package))

    def lib_push(self, _target):
        return self.push(utils.Dirs.LIB_DIR, _target)

    def framework_push(self, _target):
        return self.push(utils.Dirs.FRAMEWORK_DIR, _target)

    def priv_app_push(self, _target):
        return self.push(utils.Dirs.PRIV_APP_DIR, _target)

    def app_push(self, _target):
        return self.push(utils.Dirs.APP_DIR, _target)

    def priv_app_install(self, _target):
        return self.install(utils.Dirs.PRIV_APP_DIR, _target)

    def app_install(self, _target):
        return self.install(utils.Dirs.APP_DIR, _target)

    def app_launch(self, _simple_name):
        return self.command('adb shell monkey --pct-syskeys 0 -p {pkg} -c android.intent.category.LAUNCHER 1'
                            .format(pkg=self.__project.get_packages().get(_simple_name)))

    def fastboot(self, _image):
        msg: str
        if _image == 'dtb' and self.__project.get_name() == utils.ProjectNames.HLAB:
            msg = 'fastboot flash {img} {_root}{_from}{_to}tcc8030-android-lpd4321_sv0.1.dtb'\
                .format(_root=self.__project.get_root(),
                        _from=self.__project.get_from(),
                        _to=self.__project.get_to(),
                        img=_image)

        else:
            msg = 'fastboot flash {img} {_root}{_from}{_to}{img}.img'\
                .format(_root=self.__project.get_root(),
                        _from=self.__project.get_from(),
                        _to=self.__project.get_to(),
                        img=_image)

        log.i(msg)
        return os.system(msg)

    def fastboot_reboot(self):
        return os.system('fastboot reboot')

    def screen_capture(self) -> str:
        __format = '%Y%m%d_%H%M%S.png'
        __file = time.strftime(__format, time.localtime())
        os.system('adb shell screencap -p /data/{0}'.format(__file))
        os.system("adb pull /data/{0} {1}/Downloads".format(__file, os.getenv('HOME')))

        out_path = '{0}/Downloads/{1}'.format(os.getenv('HOME'), __file)

        if os.path.exists(out_path) is False:
            log.e('screen capture fail')
            return ''

        log.i("screen capture path = {0}".format(out_path))
        return out_path

    def broadcast(self, _action: str, _extra: str = None, _extra_value=None):
        _type = type(_extra_value)
        _extra_type: str = ''

        if _type == int:
            _extra_type = 'ei'
        elif _type == bool:
            _extra_type = 'ez'
        elif _type == str:
            _extra_type = 'es'

        if not _extra is None and not _extra_value is None:
            return self.command('adb shell am broadcast -a {action} --{type} {extra} {value}'
                                .format(action=_action,
                                        type=_extra_type,
                                        extra=_extra,
                                        value=_extra_value))
        else:
            return self.command('adb shell am broadcast -a {action}'
                                .format(action=_action))

    def key_event(self, _what: str):
        return os.system('adb shell input keyevent KEYCODE_{}'.format(_what.upper()))

    def version_name(self, _name: str):
        if len(_name.split('.')) > 1:
            return self.command('adb shell dumpsys package {} | grep versionName'
                                .format(_name)).split('\n')[0].split('=')[1]
        else:
            return self.command('adb shell dumpsys package {} | grep versionName'
                                .format(self.__project.get_packages().get(_name))).split('\n')[0].split('=')[1]

    def volume_get(self, _stream: int):
        return self.command('adb shell media volume --stream {} --get'.format(_stream))

    def volume_set(self, _stream: int, _volume: int):
        return self.command('adb shell media volume --show --stream {} --set {}'.format(_stream, _volume))

    def activity_get(self):
        return self.command("adb shell dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'")
