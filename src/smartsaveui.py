import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

import mayautils
print("imported")


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class SmartSaveUI(QtWidgets.QDialog):
    """simple UI class"""

    def __init__(self):
        """Constructor"""

        super(SmartSaveUI, self).__init__(parent=maya_main_window())
        self.scene = mayautils.SceneFile()
        print(self.scene.dir)
        print(self.scene.version)
        self.setWindowTitle("Smart Save")
        self.resize(500, 200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create widgets for our UI"""
        self.title_lbl = QtWidgets.QLabel("Smart Save")
        self.title_lbl.setStyleSheet("font: bold 20px")

        self.dir_lbl = QtWidgets.QLabel("Directory")
        self.dir_le = QtWidgets.QLineEdit()
        self.dir_le.setText(self.scene.dir)

        self.descriptor_lbl = QtWidgets.QLabel("Descriptor")
        self.descriptor_le = QtWidgets.QLineEdit()
        self.descriptor_le.setText(self.scene.descriptor)

        self.version_lbl = QtWidgets.QLabel("Versions")
        self.version_spinbox = QtWidgets.QSpinBox()
        self.version_spinbox.setValue(self.scene.version)

        self.ext_lbl = QtWidgets.QLabel("Extension")
        self.ext_le = QtWidgets.QLineEdit("ma")
        self.ext_le.setText(self.scene.ext)

        self.browse_btn = QtWidgets.QPushButton("Browse")
        self.save_btn = QtWidgets.QPushButton("Save")
        self.increment_save_btn = QtWidgets.QPushButton("Increment and Save")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        """Layout Widgets in UI"""
        self.directory_lay = QtWidgets.QHBoxLayout()
        self.directory_lay.addWidget(self.dir_lbl)
        self.directory_lay.addWidget(self.dir_le)
        self.directory_lay.addWidget(self.browse_btn)

        self.descriptor_lay = QtWidgets.QHBoxLayout()
        self.descriptor_lay.addWidget(self.descriptor_lbl)
        self.descriptor_lay.addWidget(self.descriptor_le)

        self.version_lay = QtWidgets.QHBoxLayout()
        self.version_lay.addWidget(self.version_lbl)
        self.version_lay.addWidget(self.version_spinbox)

        self.ext_lay = QtWidgets.QHBoxLayout()
        self.ext_lay.addWidget(self.ext_lbl)
        self.ext_lay.addWidget(self.ext_le)

        self.bottom_btn_lay = QtWidgets.QHBoxLayout()
        self.bottom_btn_lay.addWidget(self.increment_save_btn)
        self.bottom_btn_lay.addWidget(self.save_btn)
        self.bottom_btn_lay.addWidget(self.cancel_btn)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.title_lbl)
        self.main_layout.addLayout(self.directory_lay)
        self.main_layout.addLayout(self.descriptor_lay)
        self.main_layout.addLayout(self.version_lay)
        self.main_layout.addLayout(self.ext_lay)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.bottom_btn_lay)
        self.setLayout(self.main_layout)

    def create_connections(self):
        """Connect our widgets signals to slots"""
        self.cancel_btn.clicked.connect(self.cancel)
        self.save_btn.clicked.connect(self.save)
        self.increment_save_btn.clicked.connect(self.increment_save)
        self.browse_btn.clicked.connect(self.browse)

    def _populate_scenefile_properties(self):
        """populate teh scene file properties from the UI"""
        self.scene.dir = self.dir_le.text()
        self.scene.descriptor = self.descriptor_le.text()
        self.scene.version = self.version_spinbox.value()
        self.scene.ext = self.ext_le.text()

    @QtCore.Slot()
    def increment_save(self):
        """increment save scene file"""
        self._populate_scenefile_properties()
        self.scene.increment_and_save()

    @QtCore.Slot()
    def save(self):
        """saves scene files"""
        self._populate_scenefile_properties()
        self.scene.save()

    @QtCore.Slot()
    def browse(self):
        """browse file in a window"""
        new_directory = QtWidgets.QFileDialog.getExistingDirectory()
        self.scene.dir = new_directory
        self.dir_le.setText(self.scene.dir)

    @QtCore.Slot()
    def cancel(self):
        """quits dialog window"""
        self.close()
