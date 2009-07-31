# -*- coding: utf-8 -*-

from Source.SourceBase import *
import utils

class ArchiveSource(SourceBase):
    """ file download source"""
    filenames = []    
    def __init__(self):
        SourceBase.__init__(self)
        utils.debug( "ArchiveSource.__init__ called", 2 )

    def __localFileNames(self):
        """ collect local filenames """
        utils.debug( "ArchiveSource.__localFileNames called", 2 )

        filenames =[]

        if self.subinfo.hasTarget():
            for uri in self.subinfo.target().split():
                filenames.append( os.path.basename( uri ) )
        return filenames

    def fetch(self):
        """getting normal tarballs from SRC_URI"""
        utils.debug( "ArchiveSource.fetch called", 2 )
            
        filenames = self.__localFileNames()
        
        if ( self.noFetch ):
            utils.debug( "skipping fetch (--offline)" )
            return True
        if self.subinfo.hasTarget():
            return utils.getFiles( self.subinfo.target(), self.downloadDir() )
        else:
            return utils.getFiles( "", self.downloadDir() )

    def unpack(self):
        """unpacking all zipped(gz,zip,bz2) tarballs"""        
        utils.debug( "ArchiveSource.unpack called", 2 )

        filenames = self.__localFileNames()        
        # if using BinaryBuildSystem the files should be unpacked into imagedir
        if hasattr(self, 'buildSystemType') and self.buildSystemType == 'binary':
            destdir = self.installDir()
            utils.debug("unpacking files into image root %s" % destdir,1)
        else:
            destdir = self.workDir()
            utils.debug("unpacking files into work root %s" % destdir,1)

        if not utils.unpackFiles( self.downloadDir(), filenames, destdir ):
            return False

        return self.applyPatches()

    def sourceDir(self): 
        sourcedir = self.workDir()
        if hasattr(self, 'buildSystemType') and self.buildSystemType == 'binary':
            sourcedir = self.imageDir()

        if self.subinfo.hasTargetSourcePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.targetSourcePath())
        if utils.verbose > 1:
            print "using sourcedir: " + sourcedir
        return sourcedir

