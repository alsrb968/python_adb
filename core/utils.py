ROOT = '~/LITBIG-Z840C-JACOB/project/'

APP_DIR = 'system/app/'
PRIV_APP_DIR = 'system/priv-app/'
FRAMEWORK_DIR = 'system/framework/'
LIB_DIR = 'system/lib/'

FROM = 'from'
TO = 'to'
PORT = 'port'

DIGEN = '/dev/tty.usbserial-1301'
AVN = '/dev/tty.usbserial-FTHFJNY0'


class Directory:
    from project import Project

    __from = {
        Project.BENZ_SB: 'digen/benz/benz_silverbox_tcc8990pie/',
        Project.BENZ_SG: 'digen/benz/benz_smartglass_tcc8990pie/',
        Project.KA4: 'digen/ka4/ka4_silverbox_tcc8990pie/',
        Project.SCANIA: 'scania/avn_tcc897x_android_kk/',
        Project.DPECO: 'jy/dpeco/avn_tcc897x_android_kk/',
        Project.HLAB: 'hlab/avn_tcc803x_android_pie/'
    }

    __to = {
        Project.BENZ_SB: 'out/target/product/tcc899x/',
        Project.BENZ_SG: 'out/target/product/tcc899x/',
        Project.KA4: 'out/target/product/tcc899x/',
        Project.SCANIA: 'out/target/product/tcc897x/',
        Project.DPECO: 'out/target/product/tcc897x/',
        Project.HLAB: 'out/target/product/car_tcc803x_arm64/'
    }

    def get_from(self, project):
        return self.__from.get(project, None)

    def get_to(self, project):
        return self.__to.get(project, None)


class Port:
    from project import Project

    __port = {
        Project.BENZ_SB: DIGEN,
        Project.BENZ_SG: DIGEN,
        Project.KA4: DIGEN,
        Project.SCANIA: AVN,
        Project.DPECO: AVN,
        Project.HLAB: AVN
    }

    def get_port(self, project):
        return self.__port.get(project, None)
