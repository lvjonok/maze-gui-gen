"""Module contains tutorial window"""
import os

from PyQt5 import QtGui, QtWidgets

import source.py_ui.informationUI as informationUI  # pylint: disable=import-error
from source.tools.app_settings import (  # pylint: disable=import-error
    AppSettings,
    getMediaDirectory,
)

MEDIA_DIRECTORY = getMediaDirectory()


class InformationWindow(QtWidgets.QWidget, informationUI.Ui_InformationWidget):
    def __init__(self):
        super().__init__()

        self.settings = AppSettings()

        self.current_image = 1
        self.setupUi(self)
        self.b_nextImage.clicked.connect(self.nextImage)
        self.b_previousImage.clicked.connect(self.previousImage)
        self.locale_language = "ru"
        self.displayImage()
        self.shortcut_n_img = QtWidgets.QShortcut(QtGui.QKeySequence("Right"), self)
        self.shortcut_p_img = QtWidgets.QShortcut(QtGui.QKeySequence("Left"), self)
        self.shortcut_n_img_k = QtWidgets.QShortcut(QtGui.QKeySequence("n"), self)
        self.shortcut_p_img_k = QtWidgets.QShortcut(QtGui.QKeySequence("p"), self)
        self.shortcut_n_img.activated.connect(self.nextImage)
        self.shortcut_p_img.activated.connect(self.previousImage)
        self.shortcut_n_img_k.activated.connect(self.nextImage)
        self.shortcut_p_img_k.activated.connect(self.previousImage)
        # can close window by pressing Enter
        self.shortcutClose = QtWidgets.QShortcut(QtGui.QKeySequence("Return"), self)
        self.shortcutClose.activated.connect(self.close)
        # can close window by pressing Esc
        self.shortcutCloseE = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self)
        self.shortcutCloseE.activated.connect(self.close)

    def resizeEvent(self, event):
        # o_size = [event.oldSize().width(), event.oldSize().height()]
        c_size = [event.size().width(), event.size().height()]
        min_size = min(c_size)
        self.tutorialImage.setGeometry(
            c_size[0] // 2 - min_size // 2, 0, min_size, min_size
        )

        self.b_nextImage.move(c_size[0] - 20, round(240 / 600 * c_size[1]))
        self.b_previousImage.move(0, round(240 / 600 * c_size[1]))

    def nextImage(self):
        self.current_image += 1
        if self.current_image > 8:
            self.current_image = 1
        self.displayImage()

    def previousImage(self):
        self.current_image -= 1
        if self.current_image < 1:
            self.current_image = 8
        self.displayImage()

    def displayImage(self):
        path = self.getImagePath()
        # print(path)
        self.tutorialImage.setPixmap(QtGui.QPixmap(path))

    def getImagePath(self):
        return os.path.join(
            MEDIA_DIRECTORY,
            "out_" + str(self.locale_language) + "_" + str(self.current_image) + ".png",
        )
