"""Module contains settings window class"""

from collections import OrderedDict
from PyQt5 import QtCore, QtWidgets

import source.py_ui.settingsUI as settingsUI  # pylint: disable=import-error
from source.tools.app_settings import AppSettings  # pylint: disable=import-error
import source.tools.Const as const  # pylint: disable=import-error
from source.tools.Generator import getRobotConfiguration  # pylint: disable=import-error


class SettingsWindow(QtWidgets.QWidget, settingsUI.Ui_settingsForm):
    def __init__(self):
        super().__init__()

        self.settings = AppSettings()

        self.setupUi(self)
        self.colorLabel.mousePressEvent = self.updateValueColorLine

        self.lineCellSizeSlider.valueChanged.connect(self.updateValueLineCellSize)
        self.linePixelSizeSlider.valueChanged.connect(self.updateValueLinePixelSize)
        self.mazeCellSizeSlider.valueChanged.connect(self.updateValueMazeCellSize)
        self.MazeLoopsCheckBox.stateChanged.connect(self.updateValueMazeLoopsCheckBox)
        self.pngImageCheckBox.stateChanged.connect(self.updateValuePNGImageCheckBox)
        self.svgFieldCheckBox.stateChanged.connect(self.updateValueSVGFieldCheckBox)
        self.excersizeTime.timeChanged.connect(self.updateValueExcersizeTimelimit)
        self.applyChangesButton.clicked.connect(self.applyChanges)
        self.roboticsKitList.activated.connect(self.updateRoboticsKit)

        self.updateWidgetsOnStart()

    def updateWidgetsOnStart(self):
        time_set = self.settings.getSettings("valueExcersizeTimelimit")
        if time_set:
            time_set = list(map(int, time_set))
            self.excersizeTime.setTime(QtCore.QTime(0, time_set[0], second=time_set[1]))
        else:
            self.excersizeTime.setTime(QtCore.QTime(0, 59, second=59))
            self.updateValueExcersizeTimelimit()

        color_set = self.settings.getSettings("valueColorLine")
        if color_set:
            self.colorLine = color_set
        else:
            self.colorLine = "000000"
            self.settings.updateSettings("valueColorLine", self.color_line)

        self.colorLabel.setStyleSheet(
            "QLabel {background-color: #" + str(self.colorLine) + ";}"
        )

        params = ["valueLinePixelSize", "valueLineCellSize", "valueMazeCellSize"]

        values = [self.settings.getSettings(param) for param in params]

        if values[0]:
            self.linePixelSizeSlider.setValue(int(values[0]))
        else:
            # standart line width is 6 px
            self.linePixelSizeSlider.setValue(6)
            self.settings.updateSettings(params[0], 6)

        if values[1]:
            self.lineCellSizeSlider.setValue(int(values[1]))
        else:
            # standart line width is 2 cells
            self.lineCellSizeSlider.setValue(2)
            self.settings.updateSettings(params[1], 2)

        if values[2]:
            self.mazeCellSizeSlider.setValue(int(values[2]))
        else:
            # standart line width is 3 cells
            self.mazeCellSizeSlider.setValue(3)
            self.settings.updateSettings(params[2], 3)

        loops_set = self.settings.getSettings("valueMazeLoopsCheckBox")
        if loops_set:
            self.MazeLoopsCheckBox.setChecked(loops_set == "true")
        else:
            self.MazeLoopsCheckBox.setChecked(False)
            self.settings.updateSettings("valueMazeLoopsCheckBox", False)

        png_set = self.settings.getSettings("valuePNGImageCheckBox")
        if png_set:
            self.pngImageCheckBox.setChecked(png_set == "true")
        else:
            self.pngImageCheckBox.setChecked(False)
            self.settings.updateSettings("valuePNGImageCheckBox", False)

        svg_set = self.settings.getSettings("valueSVGFieldCheckBox")
        if svg_set:
            self.svgFieldCheckBox.setChecked(svg_set == "true")
        else:
            self.svgFieldCheckBox.setChecked(False)
            self.settings.updateSettings("valueSVGFieldCheckBox", False)

        robotics_kit = self.settings.getSettings("roboticsKit")
        self.roboticsConfig: str = ""
        if robotics_kit:
            self.roboticsKitList.setCurrentIndex(
                const.ROBOTICS_KITS.index(robotics_kit)
            )
        else:
            self.roboticsKitList.setCurrentIndex(0)
            self.updateRoboticsKit(None)
        robot_cfg = self.settings.getSettings("roboticsConfig")
        # print('rbcfg', robot_cfg)
        # print('rbrk', robotics_kit)
        if robotics_kit == "XML" and robot_cfg != "":
            self.roboticsConfig: str = robot_cfg
        else:
            self.roboticsConfig = ""
            self.settings.updateSettings("roboticsConfig", '""')

        self.settings.sync()

    def applyChanges(self):
        self.settings.sync()
        msg = QtWidgets.QMessageBox()
        if self.locale_language == "en":
            msg.setText("Your settings were saved!")
            msg.setWindowTitle("Information")
        else:
            msg.setText("Ваши настройки были сохранены")
            msg.setWindowTitle("Информация")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec_()
        self.close()

    # updates label with line pixel size
    def updateValueLinePixelSize(self):
        value = self.getSliderLinePixelSize()
        self.linePixelSizeValue.setText(
            '<html><head/><body><p align="center">' + str(value) + "</p></body></html>"
        )
        self.settings.updateSettings("valueLinePixelSize", value)

    # updates label with maze cell size
    def updateValueMazeCellSize(self):
        value = self.getSliderMazeCellSize()
        self.mazeCellSizeValue.setText(
            '<html><head/><body><p align="center">' + str(value) + "</p></body></html>"
        )
        self.settings.updateSettings("valueMazeCellSize", value)

    # updates label with line cell size
    def updateValueLineCellSize(self):
        value = self.getSliderLineCellSize()
        self.lineCellSizeValue.setText(
            '<html><head/><body><p align="center">' + str(value) + "</p></body></html>"
        )
        self.settings.updateSettings("valueLineCellSize", value)

    def updateValueMazeLoopsCheckBox(self):
        self.settings.updateSettings(
            "valueMazeLoopsCheckBox", self.MazeLoopsCheckBox.isChecked()
        )

    def updateValuePNGImageCheckBox(self):
        self.settings.updateSettings(
            "valuePNGImageCheckBox", self.pngImageCheckBox.isChecked()
        )

    def updateValueSVGFieldCheckBox(self):
        self.settings.updateSettings(
            "valueSVGFieldCheckBox", self.svgFieldCheckBox.isChecked()
        )

    def updateValueExcersizeTimelimit(self):
        self.settings.updateSettings("valueExcersizeTimelimit", self.getTimelimit())

    def rgb_to_hex(self, rgb):
        return "%02x%02x%02x" % rgb

    def getSliderMazeCellSize(self) -> int:
        return self.mazeCellSizeSlider.value()

    def getSliderLinePixelSize(self) -> int:
        return self.linePixelSizeSlider.value()

    def getSliderLineCellSize(self) -> int:
        return self.lineCellSizeSlider.value()

    def getMazeCheckBox(self):
        return self.MazeLoopsCheckBox.isChecked()

    def getPNGImageCheckBox(self):
        return self.pngImageCheckBox.isChecked()

    def getSVGFieldCheckBox(self):
        return self.svgFieldCheckBox.isChecked()

    def getTimelimit(self):
        v = self.excersizeTime.time().toString()
        # 0 - hours, 1 - minutes, 2 - seconds
        v = [int(vi) for vi in v.split(":")][1:3]
        return v

    def updateValueColorLine(self, event):
        color = QtWidgets.QColorDialog.getColor(options=QtWidgets.QColorDialog.DontUseNativeDialog)
        if color:
            rgb = color.getRgb()[0:3]
            hex_color = self.rgb_to_hex(rgb)
            self.colorLabel.setStyleSheet(
                "QLabel {background-color: #" + str(hex_color) + ";}"
            )
            self.colorLine = hex_color
            self.settings.updateSettings("valueColorLine", hex_color)

    def updateRoboticsKit(self, event):
        self.roboticsKit = self.getRoboticsKit()
        self.settings.updateSettings("roboticsKit", self.roboticsKit)
        if self.roboticsKit == "XML":
            if self.locale_language == "ru":
                info_caption = "Выберите поле со своим роботом"
            else:
                info_caption = "Select field with your robot"

            saved_last_directory = self.settings.getSettings("valueSavedLastDirectory")
            if saved_last_directory:
                dir_path = saved_last_directory
            else:
                dir_path = sys.path[0]
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                caption=info_caption,
                directory=dir_path,
                filter="Fields (*.xml)",
                options=options,
            )
            if not fileName:  # if it is not accessible
                # in case we can't remain "XML" robot kit, we change it to default
                self.roboticsKitList.setCurrentIndex(0)
                self.settings.updateSettings("roboticsKit", self.roboticsKit)
                return False

            config: OrderedDict = getRobotConfiguration(fileName)
            # print('config',config)
            if not config:  # if we could not take configuration
                # in case we can't remain "XML" robot kit, we change it to default
                msg = QtWidgets.QMessageBox()
                if self.locale_language == "en":
                    msg.setText("There are some errors with this field, select another!")
                    msg.setWindowTitle("Error")
                else:
                    msg.setText("Возникли проблемы с этим полем, выберите другое!")
                    msg.setWindowTitle("Ошибка")
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.exec_()
                self.roboticsKitList.setCurrentIndex(0)
                self.settings.updateSettings("roboticsKit", self.roboticsKit)
                return False

            # print('writing', config)
            self.settings.updateSettings("roboticsConfig", str(config))

    def getRoboticsKit(self) -> str:
        return str(self.roboticsKitList.currentText())

    def setRussian(self):
        self.locale_language = "ru"
        self.pngImageLabel.setText("Сохранять PNG превью для полей")
        self.svgFieldLabel.setText("Сохранять SVG файл для полей")
        self.MazeLoopsLabel.setText("Лабиринт с циклами")
        self.roboticsKitLabel.setText("Платформа")
        self.groupBox.setTitle("Настройки для генерации полей")
        self.lineCellSizeLabel.setText("Размер ячейки с линией")
        self.linePixelSizeLabel.setText("Ширина линии")
        self.mazeCellSizeLabel.setText("Размер ячейки для лабиринта")
        self.timelimitLabel.setText("Временное ограничение для задания (MM:SS)")
        self.lineColorLabel.setText("Цвет линии")
        self.applyChangesButton.setText("Применить изменения")

    def setEnglish(self):
        self.locale_language = "en"
        self.pngImageLabel.setText("Save PNG image with field preview")
        self.svgFieldLabel.setText("Save SVG file for each XML field")
        self.MazeLoopsLabel.setText("Maze with loops")
        self.roboticsKitLabel.setText("Robotics construction kit")
        self.groupBox.setTitle("Settings for fields generation")
        self.lineCellSizeLabel.setText("Line cell size")
        self.linePixelSizeLabel.setText("Line width")
        self.mazeCellSizeLabel.setText("Maze cell size")
        self.timelimitLabel.setText("Timelimit for excersize (MM:SS)")
        self.lineColorLabel.setText("Line color")
        self.applyChangesButton.setText("Apply changes")

    def getGenerationSettings(self) -> dict:
        """
        Function returns applied settings for every key in Const.FIELD_GENERATOR_SETTINGS_KEYS
        """
        keys: list = const.FIELD_GENERATOR_SETTINGS_KEYS
        out_dict: dict = {}

        for key in keys:
            value = self.settings.getSettings(key)
            if value:
                out_dict[key] = value
        return out_dict
