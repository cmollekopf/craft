import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Identity Management library"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/kcoreaddons"] = "default"
        self.buildDependencies["frameworks/ktextwidgets"] = "default"
        self.buildDependencies["frameworks/kxmlgui"] = "default"
        self.buildDependencies["frameworks/kconfig"] = "default"
        self.buildDependencies["frameworks/kcodecs"] = "default"
        self.buildDependencies["frameworks/kiconthemes"] = "default"
        self.buildDependencies["frameworks/kio"] = "default"
        self.buildDependencies["kde/kpimtextedit"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )