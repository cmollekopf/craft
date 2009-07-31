from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.2.3-2']:
            self.targets[ version ] = repoUrl + """/zlib-""" + version + """-bin.zip
                                """ + repoUrl + """/zlib-""" + version + """-lib.zip"""
            
        self.defaultTarget = '1.2.3-2'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
