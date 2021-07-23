#!/usr/bin/python

import sys

from core.adb import Adb
from core.project import Project


def fastboot(__adb: Adb, __name: str):
    __adb.remount()
    __adb.reboot('bootloader')
    __adb.fastboot(__name)
    __adb.fastboot_reboot()


def launch(__adb: Adb, __name: str):
    __adb.remount()
    __adb.app_launch({
        'allapps': 'com.android.allapps',
        'settings': 'com.android.settings',
        'documents': 'com.android.documentsui'
    }.get(__name))


def install(__adb: Adb, __name: str, __package: str):
    __adb.remount()
    __adb.app_install(__name)
    __adb.app_launch(__package)


def app_push(__adb: Adb, __name: str):
    __adb.remount()
    __adb.app_push(__name)
    __adb.reboot()


def priv_app_push(__adb: Adb, __name: str):
    __adb.remount()
    __adb.priv_app_push(__name)
    __adb.reboot()


def broadcast(__adb: Adb, __name: str):
    __adb.remount()
    __adb.broadcast({
        'boot_completed': 'com.litbig.action.BOOT_COMPLETED'
    }.get(__name))


def key_code(__adb: Adb, __name: str):
    __adb.remount()
    __adb.key_event(__name)


def version_name(__adb: Adb, __name: str):
    __adb.remount()
    __adb.version_name({
        'polnav': 'com.polstar.polnav6',
        'launcher': 'hanhwa.lm18i.launcher'
   }.get(__name))


if __name__ == '__main__':
    project = Project()
    adb = Adb(project)

    cmd = sys.argv[1].lower()
    input_len = len(sys.argv)
    # log.d('input len : {len}'.format(len=input_len))
    if input_len >= 3:
        name = sys.argv[2]

        if cmd == 'project':
            if len(name) > 0:
                project.set_path(name)
                adb = Adb(project)

        else:
            func = {'fastboot': fastboot,
                    'launch': launch,
                    'broadcast': broadcast,
                    'key': key_code,
                    'version': version_name}.get(cmd)

            func(adb, name)

    elif input_len >= 2:
        adb.remount()

        if cmd == 'screencap':
            adb.screen_capture()

        # ------ push ------
        elif cmd in {'automotive', 'auto'}:
            adb.framework_push('automotive.jar')
            if project.get_project() in {Project.SCANIA,
                                         Project.DPECO}:
                adb.framework_push('automotive.odex')
            else:
                adb.framework_push('automotive-service.jar')

            adb.reboot()

        elif cmd in {'automotive-service', 'autoser'}:
            adb.framework_push('automotive-service.jar')
            adb.reboot()

        elif cmd == 'systemui':
            adb.priv_app_install('SystemUI')

        elif cmd == 'wfd' \
                and project.get_project() in {Project.BENZ_SB,
                                              Project.BENZ_SG}:
            adb.priv_app_install('Litbig_WfdSink')

        elif cmd == 'settings':
            adb.priv_app_install('Settings')

        elif cmd in {'key', 'keyboard'}:
            priv_app_push(adb, 'Litbig_Keyboard')

        elif cmd in {'pkginst', 'packageinstaller'}:
            adb.priv_app_install('PackageInstaller')

        elif cmd in {"poweroff", "power"} \
                and project.get_project() in {Project.SCANIA,
                                              Project.DPECO}:
            adb.priv_app_push("Litbig_PowerOff.apk")
            adb.priv_app_push("Litbig_PowerOff.odex")
            adb.reboot()

        elif cmd == "launcher":
            if project.get_project() in {Project.SCANIA,
                                         Project.DPECO}:
                adb.priv_app_push("Litbig_Launcher.apk")
                adb.priv_app_push("Litbig_Launcher.odex")
                adb.reboot()
            elif project.get_project() == Project.HLAB:
                priv_app_push(adb, "LM18I_Launcher")

        elif cmd == 'aux' \
                and project.get_project() == Project.HLAB:
            app_push(adb, 'LM18I_AuxPlayer')

        elif cmd == 'dmb':
            app_push(adb, 'Litbig_DMB')

        elif cmd == 'bt':
            app_push(adb, 'Bluetooth')

        elif cmd in {'bg', 'background'} \
                and project.get_project() in {Project.BENZ_SB,
                                              Project.BENZ_SG}:
            app_push(adb, 'Litbig_BackgroundService')

        elif cmd == 'browser':
            install(adb, 'Browser2', 'org.chromium.webview_shell')

        elif cmd == 'camera' \
                and project.get_project() == Project.BENZ_SG:
            install(adb, 'Litbig_Camera', 'com.litbig.app.camera')

        else:
            print('not find argv')
