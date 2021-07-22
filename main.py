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


if __name__ == '__main__':
    project = Project()
    adb = Adb(project)

    # console = serial.Serial(port=ComPort, baudrate=BaudRate, timeout=3)
    app = sys.argv[1].lower()
    input_len = len(sys.argv)
    # log.d('input len : {len}'.format(len=input_len))
    # ------ project config ------
    if input_len >= 3:
        name = sys.argv[2].lower()

        if app == 'project':
            if len(name) > 0:
                project.set_path(name)
                adb = Adb(project)

        elif app == 'fastboot':
            name = sys.argv[2].lower()
            fastboot(adb, name)

    else:
        if project.get_project() is None:
            log.w('not saved project... please save project')
            sys.exit(1)

        #        if len(ComPort) > 0:
        #            try:
        #                console = serial.Serial(port=ComPort, baudrate=BaudRate, timeout=3)
        #                # if console.isOpen():
        #                #     console.write(bytes('\r\n', 'UTF-8'))
        #                #     input_data = console.read(console.inWaiting())
        #                #     consoleprint(input_data)
        #                #     console.write(bytes('su \r\n', 'UTF-8'))
        #                #     input_data = console.read(console.inWaiting())
        #                #     consoleprint(input_data)
        #                #     console.write(bytes('setprop sys.usb.config mtp,adb \r\n', 'UTF-8'))
        #                #     input_data = console.read(console.inWaiting())
        #                #     consoleprint(input_data)
        #            except Exception as error:
        #                print(error)

        if input_len >= 2:
            # ------ adb ------
            # if app == 'device':
            #    try:
            #        if console.isOpen():
            #            console.write(bytes('\r\n', 'UTF-8'))
            #            console.write(bytes('su\r\n', 'UTF-8'))
            #            console.write(bytes('setprop init.svc.adbd running\r\n', 'UTF-8'))
            #            console.write(bytes('setprop persist.sys.usb.config mtp,adb\r\n', 'UTF-8'))
            #            console.write(bytes('setprop sys.usb.config mtp,adb\r\n', 'UTF-8'))
            #            console.write(bytes('setprop sys.usb.mode usb_device\r\n', 'UTF-8'))
            #            console.write(bytes('setprop sys.usb.state mtp,adb\r\n', 'UTF-8'))
            #    except Exception as error:
            #        print(error)
            # elif app == 'host':
            #    try:
            #        if console.isOpen():
            #            console.write(bytes('\r\n', 'UTF-8'))
            #            console.write(bytes('su\r\n', 'UTF-8'))
            #            console.write(bytes('setprop persist.sys.usb.config host\r\n', 'UTF-8'))
            #            console.write(bytes('setprop sys.usb.config host\r\n', 'UTF-8'))
            #            console.write(bytes('setprop sys.usb.mode usb_host\r\n', 'UTF-8'))
            #            console.write(bytes('setprop sys.usb.state host\r\n', 'UTF-8'))
            #    except Exception as error:
            #        print(error)
            # elif app == 'wifiadb':
            #    try:
            #        if console.isOpen():
            #            console.write(bytes('\r\n', 'UTF-8'))
            #            console.write(bytes('su\r\n', 'UTF-8'))
            #            console.write(bytes('setprop service.adb.tcp.port 5555\r\n', 'UTF-8'))
            #            console.write(bytes('stop adbd\r\n', 'UTF-8'))
            #            console.write(bytes('start adbd\r\n', 'UTF-8'))
            #    except Exception as error:
            #        print(error)

            if app == 'screencap':
                adb.screen_capture()

            # ------ push ------
            elif app == 'automotive' or app == 'auto':
                adb.remount()
                adb.framework_push('automotive.jar')
                if project.get_project().__contains__(
                        {Project.SCANIA,
                         Project.DPECO}):
                    adb.framework_push('automotive.odex')
                else:
                    adb.framework_push('automotive-service.jar')

                adb.reboot()

            elif app == 'automotive-service' or app == 'autoser':
                adb.remount()
                adb.framework_push('automotive-service.jar')
                adb.reboot()

            elif app == 'framework':
                adb.remount()
                adb.framework_push('framework2.jar')
                adb.framework_push('framework2.odex')
                adb.framework_push('framework.jar')
                adb.framework_push('framework.odex')
                adb.framework_push('ext.jar')
                adb.framework_push('ext.odex')
                adb.reboot()

            elif app == 'framework-service' or app == 'frser':
                adb.remount()
                adb.framework_push('services.jar')
                adb.framework_push('services.jar.prof')
                adb.framework_push('services.core.jar')
                adb.reboot()

            elif app == 'systemui':
                adb.remount()
                adb.priv_app_install('SystemUI')

            elif app == 'wfd':
                if project.get_project().__contains__(
                        {Project.BENZ_SB,
                         Project.BENZ_SG}):
                    adb.remount()
                    adb.priv_app_install('Litbig_WfdSink')

            elif app == 'settings':
                adb.remount()
                adb.priv_app_install('Settings')

            elif app == 'key' or app == 'keyboard':
                priv_app_push(adb, 'Litbig_Keyboard')

            elif app == 'pkginst' or app == 'packageinstaller':
                adb.remount()
                adb.priv_app_install('PackageInstaller')

            elif app == "poweroff" or app == "power":
                if project.get_project().__contains__(
                        {Project.SCANIA,
                         Project.DPECO}):
                    adb.remount()
                    adb.priv_app_push("Litbig_PowerOff.apk")
                    adb.priv_app_push("Litbig_PowerOff.odex")
                    adb.reboot()

            elif app.lower() == "launcher":
                if project.get_project().__contains__(
                        {Project.SCANIA,
                         Project.DPECO}):
                    adb.remount()
                    adb.priv_app_push("Litbig_Launcher.apk")
                    adb.priv_app_push("Litbig_Launcher.odex")
                    adb.reboot()
                elif project.get_path()[utils.TO] == Project.HLAB:
                    priv_app_push(adb, "LM18I_Launcher")

            elif app == 'aux':
                if project.get_path()[utils.TO] == Project.HLAB:
                    app_push(adb, 'LM18I_AuxPlayer')

            elif app == 'dmb':
                app_push(adb, 'Litbig_DMB')

            elif app == 'bt':
                app_push(adb, 'Bluetooth')

            elif app == 'bg' or app == 'background':
                if project.get_project().__contains__(
                        {Project.BENZ_SB,
                         Project.BENZ_SG}):
                    app_push(adb, 'Litbig_BackgroundService')

            elif app == 'browser':
                install(adb, 'Browser2', 'org.chromium.webview_shell')

            elif app == 'camera':
                if project.get_project() == Project.BENZ_SG:
                    install(adb, 'Litbig_Camera', 'com.litbig.app.camera')

            else:
                print('not find argv')
