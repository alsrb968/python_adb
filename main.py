#!/usr/bin/python

import sys

from core.adb import Adb
from core.project import Project
from core import utils, log


def help():
    log.i('1 param:')
    print('\tcurrent')
    print('\tvolume')
    print('\tscreencap')
    print('\tautomotive, auto')
    print('\tautomotive-service, autoser')
    print('\tsystemui')
    print('\twfd')
    print('\tsettings')
    print('\tkey, keyboard')
    print('\tpkginst, packageinstaller')
    print('\tpoweroff, power')
    print('\tlauncher')
    print('\taux')
    print('\tdmb')
    print('\tbt')
    print('\tbg, background')
    print('\tbrowser')
    print('\tcamera')
    log.i('2 param:')
    print('\tproject <name>')
    print('\t\tbenz_sb')
    print('\t\tbenz_sg')
    print('\t\tka4')
    print('\t\tscania')
    print('\t\tdpeco')
    print('\t\thlab')
    print('\tfastboot <img>')
    print('\tlaunch <app>')
    print('\tbroadcast <action>')
    print('\tkey <code>')
    print('\tversion <app>')
    print('\tvolume <stream>')
    log.i('3 params:')
    print('\tvolume <stream> <value>')
    print('\tpolnav <extra> <value>')


def fastboot(__adb: Adb, __name: str):
    __adb.reboot('bootloader')
    __adb.fastboot(__name)
    __adb.fastboot_reboot()


def launch(__adb: Adb, __name: str):
    __adb.app_launch(__name)


def install(__adb: Adb, __name: str, __package: str):
    __adb.app_install(__name)
    __adb.app_launch(__package)


def app_push(__adb: Adb, __name: str):
    __adb.app_push(__name)
    __adb.reboot()


def priv_app_push(__adb: Adb, __name: str):
    __adb.priv_app_push(__name)
    __adb.reboot()


def broadcast(__adb: Adb, __name: str):
    __adb.broadcast({
        'boot_completed': 'com.litbig.action.BOOT_COMPLETED'
    }.get(__name))


def volume_get(__adb: Adb, __stream: str):
    log.i(__adb.volume_get(utils.STREAM_TYPE.get(__stream)))


def volume_set(__adb: Adb, __stream: str, __volume: int):
    log.i(__adb.volume_set(utils.STREAM_TYPE.get(__stream), __volume))


if __name__ == '__main__':
    project = Project()
    adb = Adb(project)

    cmd = sys.argv[1].lower()
    input_len = len(sys.argv)
    # log.d('input len : {len}'.format(len=input_len))

    if input_len >= 4:
        name = sys.argv[2]
        value = sys.argv[3]

        adb.remount()

        if cmd == 'volume':
            volume_set(adb, name, int(value))
        
        elif cmd == 'polnav':
            adb.broadcast('com.polstar.javaclient.volume.request',
                          name,
                          int(value))

    elif input_len >= 3:
        name = sys.argv[2]

        if cmd == 'project':
            if len(name) > 0:
                project.save_json(name)
                adb = Adb(project)

        elif cmd == 'key':
            adb.key_event(name)

        elif cmd == 'version':
            log.i(adb.version_name(name))

        else:
            func = {'fastboot': fastboot,
                    'launch': launch,
                    'broadcast': broadcast,
                    'volume': volume_get}.get(cmd)

            func(adb, name)

    elif input_len >= 2:
        adb.remount()
        
        if cmd == 'help':
            help()

        elif cmd == 'current':
            log.i(adb.activity_get())
        
        elif cmd == 'volume':
            for stream in utils.STREAM_TYPE:
                volume_get(adb, stream)

        elif cmd == 'screencap':
            adb.screen_capture()

        # ------ push ------
        elif cmd in {'automotive', 'auto'}:
            adb.framework_push('automotive.jar')
            if project.get_name() in {utils.ProjectNames.SCANIA,
                                      utils.ProjectNames.DPECO}:
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
                and project.get_name() in {utils.ProjectNames.BENZ_SB,
                                           utils.ProjectNames.BENZ_SG}:
            adb.priv_app_install('Litbig_WfdSink')

        elif cmd == 'settings':
            adb.priv_app_install('Settings')

        elif cmd in {'key', 'keyboard'}:
            priv_app_push(adb, 'Litbig_Keyboard')

        elif cmd in {'pkginst', 'packageinstaller'}:
            adb.priv_app_install('PackageInstaller')

        elif cmd in {"poweroff", "power"} \
                and project.get_name() in {utils.ProjectNames.SCANIA,
                                           utils.ProjectNames.DPECO}:
            adb.priv_app_push("Litbig_PowerOff.apk")
            adb.priv_app_push("Litbig_PowerOff.odex")
            adb.reboot()

        elif cmd == "launcher":
            if project.get_name() in {utils.ProjectNames.SCANIA,
                                      utils.ProjectNames.DPECO}:
                adb.priv_app_push("Litbig_Launcher.apk")
                adb.priv_app_push("Litbig_Launcher.odex")
                adb.reboot()
            elif project.get_name() == utils.ProjectNames.HLAB:
                priv_app_push(adb, "LM18I_Launcher")

        elif cmd == 'aux' \
                and project.get_name() == utils.ProjectNames.HLAB:
            app_push(adb, 'LM18I_AuxPlayer')

        elif cmd == 'dmb':
            app_push(adb, 'Litbig_DMB')

        elif cmd == 'bt':
            app_push(adb, 'Bluetooth')

        elif cmd in {'bg', 'background'} \
                and project.get_name() in {utils.ProjectNames.BENZ_SB,
                                           utils.ProjectNames.BENZ_SG}:
            app_push(adb, 'Litbig_BackgroundService')

        elif cmd == 'browser':
            install(adb, 'Browser2', 'org.chromium.webview_shell')

        elif cmd == 'camera' \
                and project.get_name() == utils.ProjectNames.BENZ_SG:
            install(adb, 'Litbig_Camera', 'com.litbig.app.camera')

        else:
            print('not find argv')
