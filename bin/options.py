## @package property handling
#
# (c) copyright 2009-2011 Ralf Habacker <ralf.habacker@freenet.de>
#
#
# properties from classes in this package could be set
#
# - by package scripts,
# - by setting the 'Options' environment variable or
# - by command line
#
# for example:
#
# in blueprints/subdir/package/file.py
#   ...
#   self.subinfo.options.cmake.openIDE=1
#
# or
#
# craft "--options=cmake.openIDE=1" --make kdewin-installer
#
# or
#
# set Options=cmake.openIDE=1
# craft --make kdewin-installer
#
# The parser in this package is able to set all attributes
#
# for example:
#
#  craft "--options=unpack.unpackIntoBuildDir=1 useBuildType=1" --make <package>
#
import utils
from CraftConfig import *
from CraftCore import CraftCore
from Blueprints.CraftPackageObject import CraftPackageObject

import configparser
import atexit

class UserOptions(object):
    _settings = None
    path = None
    _options = None

    reserved = ["version", "ignored"]


    @staticmethod
    def instance():
        if not UserOptions._settings:
            UserOptions.path = CraftCore.settings.get("Blueprints", "Settings", os.path.join(CraftCore.standardDirs.etcDir(), "BlueprintSettings.ini"))
            UserOptions._settings = configparser.ConfigParser(allow_no_value=True)
            if os.path.isfile(UserOptions.path):
                UserOptions.instance().read(UserOptions.path)
            if not UserOptions.instance().has_section("/"):
                UserOptions.instance().add_section("/")
                settings = UserOptions.instance()["/"]
                opt = Options(package=None)
                UserOptions._init_vars(settings, opt)
        return UserOptions._settings

    @staticmethod
    def _init_vars(settings, opt, prefix="") -> None:
        # TODO: what do we wan't to have in here
        for var in vars(opt):
            attr = getattr(opt, var)
            if isinstance(attr, (str, int, type(None))):
                settings[f"{prefix}{var}"] = str(attr)
            else:
                UserOptions._init_vars(settings, attr, prefix=f"{var}.")

    def __init__(self, package):
        settings = UserOptions.instance()
        self.package = package
        self.settings = settings[package.path] if settings.has_section(package.path) else None

    @staticmethod
    def setOptions(optionsIn):
        options = {}
        for o in optionsIn:
            key, value = o.split("=")
            if key.startswith("dynamic."):
                CraftCore.log.warning("Detected a deprecated setting, use the BlueprintsSettings.ini"
                                      "or don't specify the \"dynamic.\" prefix in the commandline")
                key = key[len("dynamic."):]
            options[key] = value
        UserOptions._options = options

    @staticmethod
    @atexit.register
    def __dump():
        if UserOptions._settings:
            with open(UserOptions.path, 'wt+') as configfile:
                UserOptions.instance().write(configfile)

    def __setattr__(self, key, value):
        if key in ["settings", "package"]:
            super().__setattr__(key, value)
            return
        settings = self.settings
        if not settings:
            settings = UserOptions.__init(self)
        settings[key] = value

    @staticmethod
    def __init(self):
        if not UserOptions.instance().has_section(self.package.path):
            UserOptions.instance().add_section(self.package.path)
        settings = self.settings = UserOptions.instance()[self.package.path]
        return settings

    def __getattribute__(self, name):
        if name in ["settings", "package"]:
            return super().__getattribute__(name)
        settings = self.settings
        if name in UserOptions._options:
            if not settings:
                settings = UserOptions.__init(self)
            settings[name] = UserOptions._options[name]
            return settings[name]
        if settings and name in settings:
            if name == "ignored":
                return UserOptions.instance()._convert_to_boolean(settings["ignored"])
            return settings[name]

        parent = self.package.parent
        while parent:
            out = getattr(UserOptions(parent), name)
            if not out is None:
                return out
            parent = parent.parent
        if name == "args":
            return ""
        if name not in UserOptions.reserved:
            if not settings:
                settings = UserOptions.__init(self)
            settings[name] = None
        return None

class OptionsBase(object):
    def __init__(self):
        pass

## options for enabling or disabling features of KDE
## in the future, a certain set of features make up a 'profile' together
class OptionsFeatures(OptionsBase):
    def __init__(self):
        class PhononBackend(OptionsBase):
            def __init__(self):
                ## options for the phonon backend
                self.vlc = True
                self.ds9 = False

        self.phononBackend = PhononBackend()

        ## option whether to build nepomuk
        self.nepomuk = True

        ## enable python support in several packages.
        self.pythonSupport = False

        ## stick to the gcc 4.4.7 version
        self.legacyGCC = False

        ## enable or disable the dependency to plasma
        self.fullplasma = False

        ## enable plugins of kdevelop
        self.fullkdevelop = False


## options for the fetch action
class OptionsFetch(OptionsBase):
    def __init__(self):
        ## option comment
        self.option = None
        self.ignoreExternals = False
        ## enable submodule support in git single branch mode
        self.checkoutSubmodules = False


## options for the unpack action
class OptionsUnpack(OptionsBase):
    def __init__(self):
        ## By default archives are unpackaged into the workdir.
        #  Use this option to unpack archives into recent build directory
        self.unpackIntoBuildDir = False
        #  Use this option to run 3rd party installers
        self.runInstaller = False


## options for the configure action
class OptionsConfigure(OptionsBase):
    def __init__(self):
        ## with this option additional arguments could be added to the configure commmand line
        self.args = None
        ## with this option additional arguments could be added to the configure commmand line (for static builds)
        self.staticArgs = None
        ## set source subdirectory as source root for the configuration tool.
        # Sometimes it is required to take a subdirectory from the source tree as source root
        # directory for the configure tool, which could be enabled by this option. The value of
        # this option is added to sourceDir() and the result is used as source root directory.
        self.configurePath = None
        # add build target to be included into build. This feature is cmake only and requires the
        # usage of the 'macro_optional_add_subdirectory' macro. The value is a string.
        self.onlyBuildTargets = None

        # add the cmake defines that are needed to build tests here
        self.testDefine = None

        ## run autogen in autotools
        self.bootstrap = False

        # do not use default include path
        self.noDefaultInclude = False

        ## do not use default lib path
        self.noDefaultLib = False

        ## set this attribute in case a non standard configuration
        # tool is required (supported currently by QMakeBuildSystem only)
        self.tool = False

        # do not add --prefix on msys
        self.noDefaultOptions = False

        # cflags currently only used for autotools
        self.cflags = ""

        # cxxflags currently only used for autotools
        self.cxxflags = ""

        # ldflags currently only used for autotools
        self.ldflags = ""

        # the project file, this is either a .pro for qmake or a sln for msbuild
        self.projectFile = None


## options for the make action
class OptionsMake(OptionsBase):
    def __init__(self):
        ## ignore make error
        self.ignoreErrors = None
        ## options for the make tool
        self.makeOptions = None
        ## define the basename of the .sln file in case cmake.useIDE = True
        self.slnBaseName = None
        self.supportsMultijob = True


## options for the install action
class OptionsInstall(OptionsBase):
    def __init__(self):
        ## use either make tool for installing or
        # run cmake directly for installing
        self.useMakeToolForInstall = True
        ## add DESTDIR=xxx support for autotools build system
        self.useDestDir = True


## options for the merge action
class OptionsMerge(OptionsBase):
    def __init__(self):
        ## subdir based on installDir() used as merge source directory
        self.sourcePath = None


## options for the package action
class OptionsPackage(OptionsBase):
    def __init__(self):
        ## defines the package name
        self.packageName = None
        ## defines the package version
        self.version = None
        ## use compiler in package name
        self.withCompiler = True
        ## use special packaging mode  (only for qt)
        self.specialMode = False
        ## pack also sources
        self.packSources = True
        ## pack from subdir of imageDir()
        # currently supported by SevenZipPackager
        self.packageFromSubDir = None
        ## use architecture in package name
        # currently supported by SevenZipPackager
        self.withArchitecture = False
        ## add file digests to the package located in the manifest sub dir
        # currently supported by SevenZipPackager
        self.withDigests = True
        ##disable stripping of binary files
        # needed for mysql, striping make the library unusable
        self.disableStriping = False

        ##disable the binary cache for this package
        self.disableBinaryCache = False

        ## wheter to move the plugins to bin
        self.movePluginsToBin = utils.OsUtils.isWin()


class OptionsCMake(OptionsBase):
    def __init__(self):
        ## use IDE for msvc2008 projects
        self.useIDE = False
        ## use IDE for configuring msvc2008 projects, open IDE in make action instead of running command line orientated make
        self.openIDE = False
        ## use CTest instead of the make utility
        self.useCTest = CraftCore.settings.getboolean("General", "EMERGE_USECTEST", False)


class OptionsGit(OptionsBase):
    def __init__(self):
        ## enable support for applying patches in 'format-patch' style with 'git am' (experimental support)
        self.enableFormattedPatch = False


## main option class
class Options(object):
    def __init__(self, package=None):
        ## options for the dependency generation
        self.features = OptionsFeatures()
        ## options of the fetch action
        self.fetch = OptionsFetch()
        ## options of the unpack action
        self.unpack = OptionsUnpack()
        ## options of the configure action
        self.configure = OptionsConfigure()
        ## options of the configure action
        self.make = OptionsMake()
        ## options of the install action
        self.install = OptionsInstall()
        ## options of the package action
        self.package = OptionsPackage()
        ## options of the merge action
        self.merge = OptionsMerge()
        ## options of the cmake buildSystem
        self.cmake = OptionsCMake()
        ## options of the git module
        self.git = OptionsGit()

        ## add the date to the target
        self.dailyUpdate = False

        ## has an issue with a too long path
        self.needsShortPath = False

        ## this option controls if the build type is used when creating build and install directories.
        # The following example shows the difference:
        # \code
        #                True                                False
        # work/msvc2008-RelWithDebInfo-svnHEAD     work/msvc2008-svnHEAD
        # image-msvc2008-RelWithDebInfo-svnHEAD    image-msvc2008-svnHEAD
        # \endcode
        #
        self.useBuildType = True

        ## skip the related package from debug builds
        self.disableDebugBuild = False
        ## skip the related package from release builds
        self.disableReleaseBuild = False
        ## exit if system command returns errors
        self.exitOnErrors = True

        ## there is a special option available already
        self.buildTools = False
        self.buildStatic = CraftCore.settings.getboolean("Compile", "Static")

        self.useShadowBuild = True

        #### end of user configurable part
        self.__verbose = False
        self.__errors = False

        self.dynamic = UserOptions(package) if package else None


    def isActive(self, package):
        if isinstance(package, str):
            package = CraftPackageObject.get(package)
        return not package.isIgnored()
