import info


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "beta2-20130909"
        if emergePlatform.buildArchitecture() == "x86":
            self.targets[ ver ] = "http://downloads.sourceforge.net/sourceforge/msys2/x32-msys2-%s.tar.xz" % ver
        else:
            self.targets[ ver ] = "http://downloads.sourceforge.net/sourceforge/msys2/x64-msys2-%s.tar.xz" % ver
        self.defaultTarget = ver


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)        
        self.shell = MSysShell()

    def unpack(self):
        if not BinaryPackageBase.unpack(self):
           return False
        if emergePlatform.buildArchitecture() == "x64":
            shutil.move(os.path.join( self.imageDir(), "msys64"), os.path.join( self.imageDir(), "msys"))
        else:
            shutil.move(os.path.join( self.imageDir(), "msys32"), os.path.join( self.imageDir(), "msys"))
        utils.applyPatch(self.imageDir() , os.path.join(self.packageDir(), 'cd_currentDir.diff'), '0')
        utils.copyFile(os.path.join(self.packageDir(),"msys.bat"),os.path.join(self.rootdir,"dev-utils","bin","msys.bat"))
        return True
    
    def qmerge(self):
        if not BinaryPackageBase.qmerge(self):
           return False
        self.shell.execute(".","mkpasswd -l > /etc/passwd")
        self.shell.execute(".","mkgroup  -l > /etc/group")
        return True
       
if __name__ == '__main__':
    Package().execute()