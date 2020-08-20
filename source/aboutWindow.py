"""Module contains window with useful links and licence"""

import pyperclip
from PyQt5 import QtGui, QtWidgets

import source.py_ui.aboutUI as aboutUI  # pylint: disable=import-error
from source.tools.app_settings import \
    AppSettings  # pylint: disable=import-error


class AboutWindow(QtWidgets.QWidget, aboutUI.Ui_aboutWidget):
    def __init__(self):
        super().__init__()

        self.settings = AppSettings()

        self.setupUi(self)
        self.actionAgree.clicked.connect(self.close)
        # can close window by pressing Enter
        self.shortcutClose = QtWidgets.QShortcut(
            QtGui.QKeySequence('Return'), self)
        self.shortcutClose.activated.connect(self.close)
        # can close window by pressing Esc
        self.shortcutCloseE = QtWidgets.QShortcut(
            QtGui.QKeySequence('Esc'), self)
        self.shortcutCloseE.activated.connect(self.close)

        self.telegramChannel.mousePressEvent = (self.copyLink)

    def copyLink(self, event):
        pyperclip.copy('https://t.me/maze_gui_gen')

    def setRussian(self):
        self.locale_language = 'ru'
        self.InfoLabel.setText(
            '<html><head/><body><p align="center">'
            'По вопросам свяжитесь со мной в telegram: @robot_lev'
            '</p></body></html>')
        self.telegramChannel.setText(
            '<html><head/><body><p align="center">'
            'Нажмите, чтобы скопировать ссылку на telegram канал:'
            '</p><p align="center">'
            'https://t.me/maze_gui_gen'
            '</p></body></html>')

    def setEnglish(self):
        self.locale_language = 'en'
        self.InfoLabel.setText(
            '<html><head/><body><p align="center">'
            'For any issues contact me on telegram: @robot_lev'
            '</p></body></html>')
        self.telegramChannel.setText('<html><head/><body><p align="center">'
                                     'Press to copy link to telegram channel:'
                                     '</p><p align="center">'
                                     'https://t.me/maze_gui_gen'
                                     '</p></body></html>')
