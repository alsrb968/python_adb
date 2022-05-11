import os

ROOT = '{}/LITBIG-Z840C-JACOB/project/'.format(os.getenv('HOME'))


class Dirs:
    APP_DIR = 'system/app/'
    PRIV_APP_DIR = 'system/priv-app/'
    FRAMEWORK_DIR = 'system/framework/'
    LIB_DIR = 'system/lib/'


class JsonKeys:
    ROOT = 'root'
    NAME = 'name'
    FROM = 'from'
    TO = 'to'
    PORT = 'port'
    VERSION = 'version'


class Ports:
    DIGEN = '/dev/tty.usbserial-1100'
    AVN = '/dev/tty.usbserial-11300'


class ProjectNames:
    BENZ_SB = 'benz_sb'
    BENZ_SG = 'benz_sg'
    KA4 = 'ka4'
    SCANIA = 'scania'
    DPECO = 'dpeco'
    HLAB = 'hlab'


class Streams:
    VOICE_CALL = 'voice_call'
    SYSTEM = 'system'
    RING = 'ring'
    MUSIC = 'music'
    ALARM = 'alarm'
    NOTIFICATION = 'notification'
    BLUETOOTH_SCO = 'bluetooth_sco'


class AndroidVersion:
    KITKAT = 4.4
    LOLLIPOP = 5
    M = 6
    N = 7
    O = 8
    P = 9
    Q = 10
    R = 11
    S = 12


STREAM_TYPE = {
    Streams.VOICE_CALL: 0,
    Streams.SYSTEM: 1,
    Streams.RING: 2,
    Streams.MUSIC: 3,
    Streams.ALARM: 4,
    Streams.NOTIFICATION: 5,
    Streams.BLUETOOTH_SCO: 6
}

PROJECT_PACKAGE_NAME = {
    ProjectNames.BENZ_SB: {},
    ProjectNames.BENZ_SG: {},
    ProjectNames.KA4: {},
    ProjectNames.SCANIA: {},
    ProjectNames.DPECO: {},
    ProjectNames.HLAB: {'allapps': 'com.android.allapps',
                        'settings': 'com.android.settings',
                        'documentsui': 'com.android.documentsui',
                        'polnav6': 'com.polstar.polnav6',
                        'launcher': 'hanhwa.lm18i.launcher',
                        'setup': 'hanhwa.lm18i.setup'},
}

PROJECT_FROM_DIR = {
    ProjectNames.BENZ_SB: 'digen/benz/benz_silverbox_tcc8990pie/',
    ProjectNames.BENZ_SG: 'digen/benz/benz_smartglass_tcc8990pie/',
    ProjectNames.KA4: 'digen/ka4/ka4_silverbox_tcc8990pie/',
    ProjectNames.SCANIA: 'scania/avn_tcc897x_android_kk/',
    ProjectNames.DPECO: 'jy/dpeco/avn_tcc897x_android_kk/',
    ProjectNames.HLAB: 'hlab/avn_tcc803x_android_pie/'
}

PROJECT_TO_DIR = {
    ProjectNames.BENZ_SB: 'out/target/product/tcc899x/',
    ProjectNames.BENZ_SG: 'out/target/product/tcc899x/',
    ProjectNames.KA4: 'out/target/product/tcc899x/',
    ProjectNames.SCANIA: 'out/target/product/tcc897x/',
    ProjectNames.DPECO: 'out/target/product/tcc897x/',
    ProjectNames.HLAB: 'out/target/product/car_tcc803x_arm64/'
}

PROJECT_PORT = {
    ProjectNames.BENZ_SB: Ports.DIGEN,
    ProjectNames.BENZ_SG: Ports.DIGEN,
    ProjectNames.KA4: Ports.DIGEN,
    ProjectNames.SCANIA: Ports.AVN,
    ProjectNames.DPECO: Ports.AVN,
    ProjectNames.HLAB: Ports.AVN
}

PROJECT_VERSION = {
    ProjectNames.BENZ_SB: AndroidVersion.P,
    ProjectNames.BENZ_SG: AndroidVersion.P,
    ProjectNames.KA4: AndroidVersion.P,
    ProjectNames.SCANIA: AndroidVersion.KITKAT,
    ProjectNames.DPECO: AndroidVersion.KITKAT,
    ProjectNames.HLAB: AndroidVersion.P
}
