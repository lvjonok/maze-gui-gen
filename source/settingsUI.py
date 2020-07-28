# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_settingsForm(object):
    def setupUi(self, settingsForm):
        settingsForm.setObjectName("settingsForm")
        settingsForm.setWindowModality(QtCore.Qt.NonModal)
        settingsForm.resize(700, 286)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            settingsForm.sizePolicy().hasHeightForWidth())
        settingsForm.setSizePolicy(sizePolicy)
        settingsForm.setMinimumSize(QtCore.QSize(700, 286))
        settingsForm.setMaximumSize(QtCore.QSize(700, 286))
        self.horizontalLayout = QtWidgets.QHBoxLayout(settingsForm)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(settingsForm)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.timelimitLabel = QtWidgets.QLabel(self.groupBox)
        self.timelimitLabel.setObjectName("timelimitLabel")
        self.gridLayout.addWidget(self.timelimitLabel, 5, 0, 1, 1)
        self.lineCellSizeLabel = QtWidgets.QLabel(self.groupBox)
        self.lineCellSizeLabel.setObjectName("lineCellSizeLabel")
        self.gridLayout.addWidget(self.lineCellSizeLabel, 1, 0, 1, 1)
        self.linePixelSizeSlider = QtWidgets.QSlider(self.groupBox)
        self.linePixelSizeSlider.setMinimum(1)
        self.linePixelSizeSlider.setProperty("value", 6)
        self.linePixelSizeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.linePixelSizeSlider.setObjectName("linePixelSizeSlider")
        self.gridLayout.addWidget(self.linePixelSizeSlider, 2, 1, 1, 1)
        self.lineColorLabel = QtWidgets.QLabel(self.groupBox)
        self.lineColorLabel.setObjectName("lineColorLabel")
        self.gridLayout.addWidget(self.lineColorLabel, 7, 0, 1, 1)
        self.mazeCellSizeLabel = QtWidgets.QLabel(self.groupBox)
        self.mazeCellSizeLabel.setObjectName("mazeCellSizeLabel")
        self.gridLayout.addWidget(self.mazeCellSizeLabel, 3, 0, 1, 1)
        self.excersizeTime = QtWidgets.QTimeEdit(self.groupBox)
        self.excersizeTime.setCurrentSection(
            QtWidgets.QDateTimeEdit.MinuteSection)
        self.excersizeTime.setTimeSpec(QtCore.Qt.LocalTime)
        self.excersizeTime.setTime(QtCore.QTime(0, 59, 59))
        self.excersizeTime.setObjectName("excersizeTime")
        self.gridLayout.addWidget(self.excersizeTime, 5, 1, 1, 3)
        self.MazeLoopsLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MazeLoopsLabel.sizePolicy().hasHeightForWidth())
        self.MazeLoopsLabel.setSizePolicy(sizePolicy)
        self.MazeLoopsLabel.setObjectName("MazeLoopsLabel")
        self.gridLayout.addWidget(self.MazeLoopsLabel, 0, 0, 1, 2)
        self.MazeLoopsCheckBox = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.MazeLoopsCheckBox.sizePolicy().hasHeightForWidth())
        self.MazeLoopsCheckBox.setSizePolicy(sizePolicy)
        self.MazeLoopsCheckBox.setAutoFillBackground(False)
        self.MazeLoopsCheckBox.setChecked(False)
        self.MazeLoopsCheckBox.setTristate(False)
        self.MazeLoopsCheckBox.setObjectName("MazeLoopsCheckBox")
        self.gridLayout.addWidget(self.MazeLoopsCheckBox, 0, 2, 1, 2)
        self.applyChangesButton = QtWidgets.QPushButton(self.groupBox)
        self.applyChangesButton.setObjectName("applyChangesButton")
        self.gridLayout.addWidget(self.applyChangesButton, 8, 0, 1, 1)
        self.linePixelSizeLabel = QtWidgets.QLabel(self.groupBox)
        self.linePixelSizeLabel.setMaximumSize(QtCore.QSize(16777215, 17))
        self.linePixelSizeLabel.setObjectName("linePixelSizeLabel")
        self.gridLayout.addWidget(self.linePixelSizeLabel, 2, 0, 1, 1)
        self.lineCellSizeSlider = QtWidgets.QSlider(self.groupBox)
        self.lineCellSizeSlider.setStyleSheet("QSlider::groove:vertical {\n"
                                              "    background: red;\n"
                                              "    position: absolute; /* absolutely position 4px from the left and right of the widget. setting margins on the widget should work too... */\n"
                                              "    left: 4px; right: 4px;\n"
                                              "}\n"
                                              "\n"
                                              "QSlider::handle:vertical {\n"
                                              "    height: 10px;\n"
                                              "    background: green;\n"
                                              "    margin: 0 -4px; /* expand outside the groove */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider::add-page:vertical {\n"
                                              "    background: white;\n"
                                              "}\n"
                                              "\n"
                                              "QSlider::sub-page:vertical {\n"
                                              "    background: pink;\n"
                                              "}")
        self.lineCellSizeSlider.setMinimum(1)
        self.lineCellSizeSlider.setMaximum(30)
        self.lineCellSizeSlider.setProperty("value", 2)
        self.lineCellSizeSlider.setSliderPosition(2)
        self.lineCellSizeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.lineCellSizeSlider.setObjectName("lineCellSizeSlider")
        self.gridLayout.addWidget(self.lineCellSizeSlider, 1, 1, 1, 1)
        self.linePixelSizeValue = QtWidgets.QLabel(self.groupBox)
        self.linePixelSizeValue.setObjectName("linePixelSizeValue")
        self.gridLayout.addWidget(self.linePixelSizeValue, 2, 2, 1, 2)
        self.mazeCellSizeSlider = QtWidgets.QSlider(self.groupBox)
        self.mazeCellSizeSlider.setMinimum(1)
        self.mazeCellSizeSlider.setMaximum(30)
        self.mazeCellSizeSlider.setProperty("value", 3)
        self.mazeCellSizeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.mazeCellSizeSlider.setObjectName("mazeCellSizeSlider")
        self.gridLayout.addWidget(self.mazeCellSizeSlider, 3, 1, 1, 1)
        self.lineCellSizeValue = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineCellSizeValue.sizePolicy().hasHeightForWidth())
        self.lineCellSizeValue.setSizePolicy(sizePolicy)
        self.lineCellSizeValue.setScaledContents(False)
        self.lineCellSizeValue.setObjectName("lineCellSizeValue")
        self.gridLayout.addWidget(self.lineCellSizeValue, 1, 2, 1, 2)
        self.colorLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.colorLabel.sizePolicy().hasHeightForWidth())
        self.colorLabel.setSizePolicy(sizePolicy)
        self.colorLabel.setStyleSheet("QLabel {background-color: rgb(0, 0, 0);}\n"
                                      "")
        self.colorLabel.setText("")
        self.colorLabel.setObjectName("colorLabel")
        self.gridLayout.addWidget(self.colorLabel, 7, 1, 1, 3)
        self.mazeCellSizeValue = QtWidgets.QLabel(self.groupBox)
        self.mazeCellSizeValue.setObjectName("mazeCellSizeValue")
        self.gridLayout.addWidget(self.mazeCellSizeValue, 3, 2, 1, 2)
        self.horizontalLayout.addWidget(self.groupBox)

        self.retranslateUi(settingsForm)
        QtCore.QMetaObject.connectSlotsByName(settingsForm)

    def retranslateUi(self, settingsForm):
        _translate = QtCore.QCoreApplication.translate
        settingsForm.setWindowTitle(_translate("settingsForm", "Settings"))
        self.groupBox.setTitle(_translate(
            "settingsForm", "Settings for fields generation"))
        self.timelimitLabel.setText(_translate(
            "settingsForm", "Timelimit for excersize"))
        self.lineCellSizeLabel.setText(_translate(
            "settingsForm", "Line cell size (in Trik Studio cells)"))
        self.lineColorLabel.setText(_translate("settingsForm", "Line color"))
        self.mazeCellSizeLabel.setText(_translate(
            "settingsForm", "Maze cell size (in Trik Studio cells)"))
        self.excersizeTime.setDisplayFormat(
            _translate("settingsForm", "mm:ss"))
        self.MazeLoopsLabel.setText(
            _translate("settingsForm", "Map with loops"))
        self.MazeLoopsCheckBox.setText(_translate("settingsForm", "True"))
        self.applyChangesButton.setText(
            _translate("settingsForm", "Apply changes"))
        self.linePixelSizeLabel.setText(_translate(
            "settingsForm", "<html><head/><body><p>Line width (pixels)</p></body></html>"))
        self.lineCellSizeSlider.setToolTip(_translate(
            "settingsForm", "<html><head/><body><p><br/></p></body></html>"))
        self.linePixelSizeValue.setText(_translate(
            "settingsForm", "<html><head/><body><p align=\"center\">6</p></body></html>"))
        self.mazeCellSizeSlider.setToolTip(_translate(
            "settingsForm", "<html><head/><body><p><br/></p></body></html>"))
        self.lineCellSizeValue.setText(_translate(
            "settingsForm", "<html><head/><body><p align=\"center\">2</p></body></html>"))
        self.mazeCellSizeValue.setText(_translate(
            "settingsForm", "<html><head/><body><p align=\"center\">3</p></body></html>"))
