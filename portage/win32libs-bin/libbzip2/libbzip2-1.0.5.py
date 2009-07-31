from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.0.5-1']:
            self.targets[ version ] = repoUrl + """/libbzip2-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/libbzip2-""" + version + """-lib.tar.bz2"""

            
        self.defaultTarget = '1.0.5-1'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
