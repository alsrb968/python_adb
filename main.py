import argparse

from core import utils, log
from core.adb import Adb
from core.project import Project

project = Project()
adb = Adb(project)


def __fastboot(images):
    if len(images) > 0:
        adb.reboot('bootloader')
        for img in images:
            print(img)
            adb.fastboot(img)
        adb.fastboot_reboot()
    else:
        log.w("fastboot do nothing")


def __install(__name: str, __package: str):
    adb.app_install(__name)
    adb.app_launch(__package)


def __uninstall(name: str):
    adb.uninstall(project.get_packages().get(name))


def __push(_type: str, names: str):
    if len(names) < 1:
        return

    print(_type)
    for name in names:
        if _type == 'app':
            if project.get_version() == utils.AndroidVersion.KITKAT:
                adb.app_push(name + '.apk')
                adb.app_push(name + '.odex')
                print(name + '.apk, ' + name + '.odex')
            else:
                adb.app_push(name)
                print(name)

        elif _type == 'priv':
            if project.get_version() == utils.AndroidVersion.KITKAT:
                adb.priv_app_push(name + '.apk')
                adb.priv_app_push(name + '.odex')
                print(name + '.apk, ' + name + '.odex')
            else:
                adb.priv_app_push(name)
                print(name)

        elif _type == 'lib':
            adb.lib_push(name)
            print(name)

        elif _type == 'framework':
            adb.framework_push(name)
            print(name)

        else:
            return

    adb.reboot()


def __broadcast(__name: str):
    adb.broadcast({
                      'boot_completed': 'com.litbig.action.BOOT_COMPLETED'
                  }.get(__name))


def __volume(stream: str = None, volume: int = None):
    if not stream and not volume:
        for _stream in utils.STREAM_TYPE:
            log.i(adb.volume_get(utils.STREAM_TYPE.get(_stream)) + '\n')

    elif stream and not volume:
        log.i(adb.volume_get(utils.STREAM_TYPE.get(stream)))

    elif stream and volume:
        log.i(adb.volume_set(utils.STREAM_TYPE.get(stream), volume))


parser = argparse.ArgumentParser(usage='이렇게 씁니다.', description='Argparse Tutorial')
# argument는 원하는 만큼 추가한다.
parser.add_argument('--screencap', action='store_true', help='capture current screen, save at Download')
parser.add_argument('--volume', nargs='*', type=str, help='"all"= get volume all, '
                                                          '<type>= get volume type, '
                                                          '<type, vol>= set volume type on vol')
parser.add_argument('--project', type=str, help='select project')
parser.add_argument('--version', type=str, help='get application version name')
parser.add_argument('--key', type=str, help='transmit key event')
parser.add_argument('--fastboot', nargs='*', type=str, help='fastboot img(s), dtb(s)...')
parser.add_argument('--launch', type=str, help='launch application by package name')
parser.add_argument('--broadcast', nargs='*', type=str, help='broadcast message only action or action with extra')
parser.add_argument('--activity', action='store_true', help='get current activity name')
parser.add_argument('--push', nargs='*', type=str, help='push app, priv-app, lib, framework')
parser.add_argument('--boot_completed', action='store_true', help='send broadcast litbig BOOT_COMPLETED')
parser.add_argument('--tab')

args = parser.parse_args()

if __name__ == '__main__':
    print(args)

    if args.screencap:
        adb.screen_capture()

    elif args.volume:
        if len(args.volume) == 1:
            if args.volume[0] == 'all':
                __volume()
            else:
                __volume(stream=args.volume[0])
        elif len(args.volume) == 2:
            __volume(stream=args.volume[0], volume=args.volume[1])

    elif args.project:
        project.save_json(args.project)
        adb = Adb(project)

    elif args.version:
        log.i(adb.version_name(args.version))

    elif args.key:
        adb.key_event(args.key)

    elif args.fastboot:
        __fastboot(args.fastboot)

    elif args.launch:
        adb.app_launch(args.launch)

    elif args.broadcast:
        if len(args.broadcast) == 1:
            adb.broadcast(_action=args.broadcast[0])
        else:
            adb.broadcast(_action=args.broadcast[0], _extra=args.broadcast[1], _extra_value=args.broadcast[2])

    elif args.activity:
        log.i(adb.activity_get())

    elif args.push:
        if len(args.push) >= 1:
            __push(args.push[0], args.push[1:])

    elif args.boot_completed:
        __broadcast('boot_completed')
