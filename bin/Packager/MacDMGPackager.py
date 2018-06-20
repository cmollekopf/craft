from Packager.CollectionPackagerBase import *
from Utils import CraftHash

class MacDMGPackager( CollectionPackagerBase ):

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__(self, whitelists, blacklists)

    def _setDefaults(self):
        # TODO: Fix defaults
        self.defines.setdefault("apppath", "")
        self.defines.setdefault("appname", self.package.name.lower())


    def macdeployqt(self, appPath, targetLibdir, env):
        if not utils.systemWithoutShell(["dylibbundler", "-of", "-b", "-p", "@executable_path/../Frameworks", "-d", targetLibdir, "-x", f"{appPath}/Contents/MacOS/{self.defines['appname']}"], env=env):
            CraftCore.log.warning("Failed to run dylibbundler")

        if not utils.systemWithoutShell(["macdeployqt", appPath,  "-always-overwrite", "-dmg", "-verbose=2"], env=env):
            CraftCore.log.warning("Failed to run macdeployqt!")


    def createPackage(self):
        """ create a package """
        CraftCore.log.debug("packaging using the MacDMGPackager")

        self.internalCreatePackage()

        self._setDefaults()


        archive = self.archiveDir()
        appPath = os.path.join(archive, self.defines['apppath'], f"{self.defines['appname']}.app")
        if os.path.exists(os.path.join(archive, "lib/plugins")):
            utils.mergeTree(os.path.join(archive, "lib/plugins"), os.path.join(appPath, "Contents/PlugIns/"))
        targetLibdir = os.path.join(appPath, "Contents/Frameworks/")
        if not os.path.exists(targetLibdir):
            os.makedirs(targetLibdir)
        if os.path.exists(os.path.join(archive, "lib")):
            utils.mergeTree(os.path.join(archive, "lib"), targetLibdir)
        if os.path.exists(os.path.join(archive, "share")):
            utils.mergeTree(os.path.join(archive, "share"), os.path.join(appPath, "Contents/Resources/"))
        utils.mergeTree(os.path.join(archive, "bin"), os.path.join(appPath, "Contents/MacOS/"))

        env = os.environ
        env['DYLD_LIBRARY_PATH'] = os.path.join(CraftStandardDirs.craftRoot(), "lib")

        self.macdeployqt(appPath, targetLibdir, env);

        dmgSrc = appPath.replace(".app", ".dmg")
        dmgDest = os.path.join(self.packageDestinationDir(), os.path.basename(dmgSrc))
        utils.copyFile(dmgSrc, dmgDest, linkOnly=False)
        CraftHash.createDigestFiles(dmgDest)

        return True
