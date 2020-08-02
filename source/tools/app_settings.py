"""Module contains wrapped QtSettings and MEDIA_DIRECTORY"""

from PyQt5 import QtCore

import source.media as path_images  # pylint: disable=import-error


def getMediaDirectory():
    # if getattr(sys, 'frozen', False):   # running as compiled
    #     MEDIA_DIRECTORY = os.path.join(sys._MEIPASS, 'source',  # pylint: disable=protected-access, no-member
    #                                    'media')
    # else:
    #     MEDIA_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source',
    #                                    'media')
    # print(path_images.__path__[0])
    return path_images.__path__[0]


class AppSettings:
    def __init__(self):
        self.settings = QtCore.QSettings('maze-gui-generator')

    def getSettings(self, param):
        return self.settings.value(param)

    def updateSettings(self, param, value):
        self.settings.setValue(param, value)

    def sync(self):
        self.settings.sync()
