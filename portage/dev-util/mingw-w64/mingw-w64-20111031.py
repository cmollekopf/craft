import utils
import shutil
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ "20111031", "20111101" ]:
            self.targets[ver] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/mingw-w64-bin_x86_64-mingw_"+ver+"_sezero.zip"
        self.targets["4.7.1"] = "http://winkde.org/~pvonreth/downloads/%20x86_64-w64-mingw32-gcc-4.7.1-release-win64_rubenvb-crt-2.0.4.7z"

        self.defaultTarget = "4.7.1"

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)


if __name__ == '__main__':
    Package().execute()
