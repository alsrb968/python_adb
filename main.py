#!/usr/bin/python

import sys
from core import log, utils
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
    __adb.broadcast(__name)


def key_code(__adb: Adb, __name: str):
    __adb.remount()
    __adb.key_event(__name)


def version_name(__adb: Adb, __name: str):
    __adb.remount()
    __adb.version_name(__name)


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

    else:
        if project.get_project() is None:
            log.w('not saved project... please save project')
            exit(-1)

        if input_len >= 2:

            if cmd == 'screencap':
                adb.screen_capture()

            # ------ push ------
            elif cmd == 'automotive' or cmd == 'auto':
                adb.remount()
                adb.framework_push('automotive.jar')
                if project.get_project().__contains__(
                        {Project.SCANIA,
                         Project.DPECO}):
                    adb.framework_push('automotive.odex')
                else:
                    adb.framework_push('automotive-service.jar')

                adb.reboot()

            elif cmd == 'automotive-service' or cmd == 'autoser':
                adb.remount()
                adb.framework_push('automotive-service.jar')
                adb.reboot()

            elif cmd == 'framework':
                adb.remount()
                adb.framework_push('framework2.jar')
                adb.framework_push('framework2.odex')
                adb.framework_push('framework.jar')
                adb.framework_push('framework.odex')
                adb.framework_push('ext.jar')
                adb.framework_push('ext.odex')
                adb.reboot()

            elif cmd == 'framework-service' or cmd == 'frser':
                adb.remount()
                adb.framework_push('services.jar')
                adb.framework_push('services.jar.prof')
                adb.framework_push('services.core.jar')
                adb.reboot()

            elif cmd == 'systemui':
                adb.remount()
                adb.priv_app_install('SystemUI')

            elif cmd == 'wfd':
                if project.get_project().__contains__(
                        {Project.BENZ_SB,
                         Project.BENZ_SG}):
                    adb.remount()
                    adb.priv_app_install('Litbig_WfdSink')

            elif cmd == 'settings':
                adb.remount()
                adb.priv_app_install('Settings')

            elif cmd == 'key' or cmd == 'keyboard':
                priv_app_push(adb, 'Litbig_Keyboard')

            elif cmd == 'pkginst' or cmd == 'packageinstaller':
                adb.remount()
                adb.priv_app_install('PackageInstaller')

            elif cmd == "poweroff" or cmd == "power":
                if project.get_project().__contains__(
                        {Project.SCANIA,
                         Project.DPECO}):
                    adb.remount()
                    adb.priv_app_push("Litbig_PowerOff.apk")
                    adb.priv_app_push("Litbig_PowerOff.odex")
                    adb.reboot()

            elif cmd == "launcher":
                if project.get_project().__contains__(
                        {Project.SCANIA,
                         Project.DPECO}):
                    adb.remount()
                    adb.priv_app_push("Litbig_Launcher.apk")
                    adb.priv_app_push("Litbig_Launcher.odex")
                    adb.reboot()
                elif project.get_path()[utils.TO] == Project.HLAB:
                    priv_app_push(adb, "LM18I_Launcher")

            elif cmd == 'aux':
                if project.get_path()[utils.TO] == Project.HLAB:
                    app_push(adb, 'LM18I_AuxPlayer')

            elif cmd == 'dmb':
                app_push(adb, 'Litbig_DMB')

            elif cmd == 'bt':
                app_push(adb, 'Bluetooth')

            elif cmd == 'bg' or cmd == 'background':
                if project.get_project().__contains__(
                        {Project.BENZ_SB,
                         Project.BENZ_SG}):
                    app_push(adb, 'Litbig_BackgroundService')

            elif cmd == 'browser':
                install(adb, 'Browser2', 'org.chromium.webview_shell')

            elif cmd == 'camera':
                if project.get_project() == Project.BENZ_SG:
                    install(adb, 'Litbig_Camera', 'com.litbig.app.camera')

            else:
                print('not find argv')
