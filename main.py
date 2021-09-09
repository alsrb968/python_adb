#!/usr/bin/python

import sys

from core.adb import Adb
from core.project import Project
from core import utils, log


project = Project()
adb = Adb(project)


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


def fastboot(*images):
    if len(images) > 0:
        adb.reboot('bootloader')
        for img in images:
            adb.fastboot(img)
        adb.fastboot_reboot()
    else:
        log.w("fastboot do nothing")


def install(__name: str, __package: str):
    adb.app_install(__name)
    adb.app_launch(__package)


def uninstall(name: str):
    adb.uninstall(project.get_packages().get(name))


def push(type: str, *names: str):
    if len(names) > 0:
        for name in names:
            if type == 'app':
                adb.app_push(name)

            elif type == 'priv':
                adb.priv_app_push(name)

            elif type == 'lib':
                adb.lib_push(name)

            elif type == 'framework':
                adb.framework_push(name)

            else:
                return
    else:
        return

    adb.reboot()


def broadcast(__name: str):
    adb.broadcast({
        'boot_completed': 'com.litbig.action.BOOT_COMPLETED'
    }.get(__name))


def volume(stream: str = None, volume: int = None):
    if not stream and not volume:
        for _stream in utils.STREAM_TYPE:
            log.i(adb.volume_get(utils.STREAM_TYPE.get(_stream)))

    elif stream and not volume:
        log.i(adb.volume_get(utils.STREAM_TYPE.get(stream)))

    elif stream and volume:
        log.i(adb.volume_set(utils.STREAM_TYPE.get(stream), volume))


if __name__ == '__main__':
    cmd = sys.argv[1].lower()
    input_len = len(sys.argv)
    # log.d('input len : {len}'.format(len=input_len))

    if input_len >= 4:
        name = sys.argv[2]
        value = sys.argv[3]

        if cmd == 'volume':
            volume(stream=name, volume=int(value))
        
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

        elif cmd == 'version':
            log.i(adb.version_name(name))

        else:
            func = {'key': adb.key_event,
                    'fastboot': fastboot,
                    'launch': adb.app_launch,
                    'broadcast': broadcast,
                    'volume': volume}.get(cmd)

            func(name)

    elif input_len >= 2:

        if cmd == 'help':
            help()

        elif cmd == 'current':
            log.i(adb.activity_get())
        
        elif cmd == 'volume':
            for stream in utils.STREAM_TYPE:
                volume(stream=stream)

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
            push('framework', 'automotive-service.jar')

        elif cmd == 'systemui':
            adb.priv_app_install('SystemUI')

        elif cmd == 'wfd' \
                and project.get_name() in {utils.ProjectNames.BENZ_SB,
                                           utils.ProjectNames.BENZ_SG}:
            adb.priv_app_install('Litbig_WfdSink')

        elif cmd == 'settings':
            adb.priv_app_install('Settings')

        elif cmd in {'key', 'keyboard'}:
            push('priv', 'Litbig_Keyboard')

        elif cmd in {'pkginst', 'packageinstaller'}:
            adb.priv_app_install('PackageInstaller')

        elif cmd in {"poweroff", "power"} \
                and project.get_name() in {utils.ProjectNames.SCANIA,
                                           utils.ProjectNames.DPECO}:
            push('priv', 'Litbig_PowerOff.apk', 'Litbig_PowerOff.odex')

        elif cmd == "launcher":
            if project.get_name() in {utils.ProjectNames.SCANIA,
                                      utils.ProjectNames.DPECO}:
                push('priv', 'Litbig_Launcher.apk', 'Litbig_Launcher.odex')
            elif project.get_name() == utils.ProjectNames.HLAB:
                push('priv', 'LM18I_Launcher')

        elif cmd == 'aux' \
                and project.get_name() == utils.ProjectNames.HLAB:
            push('app', 'LM18I_AuxPlayer')

        elif cmd == 'dmb':
            push('app', 'Litbig_DMB')

        elif cmd == 'bt':
            push('app', 'Bluetooth')

        elif cmd in {'bg', 'background'} \
                and project.get_name() in {utils.ProjectNames.BENZ_SB,
                                           utils.ProjectNames.BENZ_SG}:
            push('app', 'Litbig_BackgroundService')

        elif cmd == 'browser':
            install('Browser2', 'org.chromium.webview_shell')

        elif cmd == 'camera' \
                and project.get_name() == utils.ProjectNames.BENZ_SG:
            install('Litbig_Camera', 'com.litbig.app.camera')

        else:
            print('not find argv')
