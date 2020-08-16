"""Module contains settings window class"""

from PyQt5 import QtCore, QtWidgets

import source.py_ui.settingsUI as settingsUI  # pylint: disable=import-error
from source.tools.app_settings import \
    AppSettings  # pylint: disable=import-error
import source.tools.Const as const  # pylint: disable=import-error

class SettingsWindow(QtWidgets.QWidget, settingsUI.Ui_settingsForm):
    def __init__(self):
        super().__init__()

        self.settings = AppSettings()

        self.setupUi(self)
        self.colorLabel.mousePressEvent = (self.controlColor)

        self.lineCellSizeSlider.valueChanged.connect(
            self.updateValueLineCellSize)
        self.linePixelSizeSlider.valueChanged.connect(
            self.updateValueLinePixelSize)
        self.mazeCellSizeSlider.valueChanged.connect(
            self.updateValueMazeCellSize)
        self.MazeLoopsCheckBox.stateChanged.connect(
            self.updateValueMazeLoopsCheckBox)
        self.excersizeTime.timeChanged.connect(
            self.updateValueExcersizeTimelimit)
        self.applyChangesButton.clicked.connect(self.applyChanges)
        self.roboticsKitList.activated.connect(self.updateRoboticsKit)

        self.updateWidgetsOnStart()

    def updateWidgetsOnStart(self):
        time_set = self.settings.getSettings('valueExcersizeTimelimit')
        if time_set:
            time_set = list(map(int, time_set))
            self.excersizeTime.setTime(QtCore.QTime(
                0, time_set[0], second=time_set[1]))
        else:
            self.excersizeTime.setTime(QtCore.QTime(0, 59, second=59))

        color_set = self.settings.getSettings('valueColorLine')
        if color_set:
            self.colorLine = color_set
        else:
            self.colorLine = "000000"
        self.colorLabel.setStyleSheet(
            'QLabel {background-color: #' + str(self.colorLine) + ';}')

        params = [
            self.settings.getSettings('valueLinePixelSize'),
            self.settings.getSettings('valueLineCellSize'),
            self.settings.getSettings('valueMazeCellSize')
        ]

        if params[0]:
            self.linePixelSizeSlider.setValue(int(params[0]))
        else:
            # standart line width is 6 px
            self.linePixelSizeSlider.setValue(6)

        if params[1]:
            self.lineCellSizeSlider.setValue(int(params[1]))
        else:
            # standart line width is 2 cells
            self.lineCellSizeSlider.setValue(2)

        if params[2]:
            self.mazeCellSizeSlider.setValue(int(params[2]))
        else:
            # standart line width is 3 cells
            self.mazeCellSizeSlider.setValue(3)

        loops_set = self.settings.getSettings('valueMazeLoopsCheckBox')
        if loops_set:
            self.MazeLoopsCheckBox.setChecked(loops_set == "true")

        robotics_kit = self.settings.getSettings('roboticsKit')
        if robotics_kit:
            self.roboticsKitList.setCurrentIndex(const.ROBOTICS_KITS.index(robotics_kit))

    def applyChanges(self):
        self.settings.sync()
        msg = QtWidgets.QMessageBox()
        if self.locale_language == 'en':
            msg.setText('Your settings were saved!')
            msg.setWindowTitle('Information')
        else:
            msg.setText('Ваши настройки были сохранены')
            msg.setWindowTitle('Информация')
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec_()
        self.close()

    # updates label with line pixel size
    def updateValueLinePixelSize(self):
        value = self.getSliderLinePixelSize()
        self.linePixelSizeValue.setText("<html><head/><body><p align=\"center\">" +
                                        str(value) + "</p></body></html>")
        self.settings.updateSettings('valueLinePixelSize', value)

    # updates label with maze cell size
    def updateValueMazeCellSize(self):
        value = self.getSliderMazeCellSize()
        self.mazeCellSizeValue.setText("<html><head/><body><p align=\"center\">" +
                                       str(value) + "</p></body></html>")
        self.settings.updateSettings('valueMazeCellSize', value)

    # updates label with line cell size
    def updateValueLineCellSize(self):
        value = self.getSliderLineCellSize()
        self.lineCellSizeValue.setText("<html><head/><body><p align=\"center\">" +
                                       str(value) + "</p></body></html>")
        self.settings.updateSettings('valueLineCellSize', value)

    def updateValueMazeLoopsCheckBox(self):
        self.settings.updateSettings(
            'valueMazeLoopsCheckBox', self.MazeLoopsCheckBox.isChecked())

    def updateValueExcersizeTimelimit(self):
        self.settings.updateSettings(
            'valueExcersizeTimelimit', self.getTimelimit())

    def rgb_to_hex(self, rgb):
        return '%02x%02x%02x' % rgb

    def getSliderMazeCellSize(self) -> int:
        return self.mazeCellSizeSlider.value()

    def getSliderLinePixelSize(self) -> int:
        return self.linePixelSizeSlider.value()

    def getSliderLineCellSize(self) -> int:
        return self.lineCellSizeSlider.value()

    def getMazeCheckBox(self):
        return self.MazeLoopsCheckBox.isChecked()

    def getTimelimit(self):
        v = self.excersizeTime.time().toString()
        # 0 - hours, 1 - minutes, 2 - seconds
        v = [int(vi) for vi in v.split(':')][1:3]
        return v

    def controlColor(self, event):
        color = QtWidgets.QColorDialog.getColor()
        if color:
            rgb = (color.getRgb()[0:3])
            hex_color = self.rgb_to_hex(rgb)
            self.colorLabel.setStyleSheet(
                'QLabel {background-color: #' + str(hex_color) + ';}')
            self.colorLine = hex_color
            self.settings.updateSettings('valueColorLine', hex_color)

    def updateRoboticsKit(self, event):
        self.roboticsKit = self.getRoboticsKit()
        self.settings.updateSettings('roboticsKit', self.roboticsKit)

    def getRoboticsKit(self) -> str:
        return str(self.roboticsKitList.currentText())

    def setRussian(self):
        self.locale_language = 'ru'
        self.roboticsKitLabel.setText('Платформа')
        self.MazeLoopsLabel.setText('Лабиринт с циклами')
        self.groupBox.setTitle('Настройки для генерации полей')
        self.lineCellSizeLabel.setText('Размер ячейки с линией')
        self.linePixelSizeLabel.setText('Ширина линии')
        self.mazeCellSizeLabel.setText('Размер ячейки для лабиринта')
        self.timelimitLabel.setText('Временное ограничение для задания (MM:SS)')
        self.lineColorLabel.setText('Цвет линии')
        self.applyChangesButton.setText('Применить изменения')

    def setEnglish(self):
        self.locale_language = 'en'
        self.roboticsKitLabel.setText('Robotics construction kit')
        self.MazeLoopsLabel.setText('Maze with loops')
        self.groupBox.setTitle('Settings for fields generation')
        self.lineCellSizeLabel.setText('Line cell size')
        self.linePixelSizeLabel.setText('Line width')
        self.mazeCellSizeLabel.setText('Maze cell size')
        self.timelimitLabel.setText('Timelimit for excersize (MM:SS)')
        self.lineColorLabel.setText('Line color')
        self.applyChangesButton.setText('Apply changes')
