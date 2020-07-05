import logging
import os
import maya.cmds as cmds

import pymel.core as pmc
from pymel.core.system import Path
from pymel.core.system import versions


log = logging.getLogger(__name__)


class SceneFile(object):
    """Class used to to represent a DCC software scene file

    The class will be a convenient object that we can use to manipulate our 
    scene files. Examples features include the ability to predefine our naming 
    conventions and automatically increment our versions.

    Attributes:
        dir (Path, optional): Directory to the scene file. Defaults to ''.
        descriptor (str, optional): Short descriptor of the scene file. 
            Defaults to "main".
        version (int, optional): Version number. Defaults to 1.
        ext (str, optional): Extension. Defaults to "ma"

    """
    print("inside")

    def __init__(self, dir='', descriptor='main', version=1, ext="ma"):
        """Initialises our attributes when class is instantiated.

        If the scene has not been saved, initialise the attributes based on 
        the defaults. Otherwise, if the scene is already saved, initialise 
        attributes based on the file name of the opened scene.

        """
        print("inside mayautils")
        file_path = cmds.file(q=True, sn=True)
        if file_path == "":
            self._dir = Path(dir)
            print(self._dir)
            self.descriptor = descriptor
            self.version = version
            self.ext = ext
        else:
            component = os.path.split(file_path)
            self._dir = component[0]
            p_name = component[1].split('_v')
            self.descriptor = p_name[0]
            tail = p_name[1].split('.')
            self.version = int(tail[0])
            self.ext = tail[1]

    @property
    def dir(self):
        print("getting")
        log.debug(self._dir)
        return self._dir

    @dir.setter
    def dir(self, val):
        print("setting")
        self._dir = Path(val)

    def basename(self):
        """Return a scene file name.

        e.g. ship_001.ma, car_011.hip

        Returns:
            str: The name of the scene file.

        """
        name_pattern = "{descriptor}_{version:03d}.{ext}"
        name = name_pattern.format(descriptor=self.descriptor,
                                   version=self.version,
                                   ext=self.ext)
        return name

    def path(self):
        """The function returns a path to scene file.

        This includes the drive letter, any directory path and the file name.

        Returns:
            Path: The path to the scene file.

        """

        return Path(self.dir) / self.basename()

    def save(self):
        """Saves the scene file.

        Returns:
            Path: The path to the scene file if successful, None, otherwise.

        """
        try:
            Path = self.dir + "\\" + self.descriptor + '_v0' + str(self.version) + '.' + self.ext
            pmc.system.saveAs(Path)
        except RuntimeError:
            log.warning("Missing directories. Creating directories.")
            self.dir.makedirs_p()
            Path = self.dir + "\\" + self.descriptor + '_v0' + str(self.version) + '.' + self.ext
            pmc.system.saveAs(Path)

    def increment_and_save(self):
        """Increments the version and saves the scene file.

        If existing versions of a file already exist, it should increment 
        from the largest number available in the folder.

        Returns:
            Path: The path to the scene file if successful, None, otherwise.
        """
        CurrentVersion = self.version
        for f in self.dir.files('*.ma'):
            component = os.path.split(f)
            Directory = component[0]
            filename = component[1].split('_v')
            Descriptor = filename[0]
            tail = filename[1].split('.')
            Version = int(tail[0])
            if self.descriptor == Descriptor:
                if CurrentVersion < Version:
                    CurrentVersion = Version
        CurrentVersion = CurrentVersion + 1
        Path = self.dir + "\\" + self.descriptor + '_v0' + str(CurrentVersion) + '.' + self.ext
        pmc.system.saveAs(Path)


