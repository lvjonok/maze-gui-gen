"""!/usr/bin/env python3"""

import sys

from PyQt5 import QtWidgets

from source.mainWindow import MazeGenApp


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    window = MazeGenApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
