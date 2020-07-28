# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutApp.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_aboutWidget(object):
    def setupUi(self, aboutWidget):
        aboutWidget.setObjectName("aboutWidget")
        aboutWidget.resize(439, 517)
        aboutWidget.setMinimumSize(QtCore.QSize(439, 517))
        aboutWidget.setMaximumSize(QtCore.QSize(439, 517))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../maze.ico"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        aboutWidget.setWindowIcon(icon)
        self.verticalLayoutWidget = QtWidgets.QWidget(aboutWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 452, 521))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(
            QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelHelp = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.labelHelp.setMinimumSize(QtCore.QSize(441, 364))
        self.labelHelp.setMaximumSize(QtCore.QSize(441, 364))
        self.labelHelp.setObjectName("labelHelp")
        self.verticalLayout.addWidget(self.labelHelp)
        self.InfoLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.InfoLabel.setScaledContents(True)
        self.InfoLabel.setObjectName("InfoLabel")
        self.verticalLayout.addWidget(self.InfoLabel)
        self.telegramChannel = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.telegramChannel.sizePolicy().hasHeightForWidth())
        self.telegramChannel.setSizePolicy(sizePolicy)
        self.telegramChannel.setScaledContents(True)
        self.telegramChannel.setObjectName("telegramChannel")
        self.verticalLayout.addWidget(self.telegramChannel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.actionAgree = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.actionAgree.sizePolicy().hasHeightForWidth())
        self.actionAgree.setSizePolicy(sizePolicy)
        self.actionAgree.setObjectName("actionAgree")
        self.horizontalLayout.addWidget(self.actionAgree)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(aboutWidget)
        QtCore.QMetaObject.connectSlotsByName(aboutWidget)

    def retranslateUi(self, aboutWidget):
        _translate = QtCore.QCoreApplication.translate
        aboutWidget.setWindowTitle(_translate(
            "aboutWidget", "About maze-gui-generator"))
        self.labelHelp.setText(_translate("aboutWidget", "<html><head/><body><p align=\"center\"><br/></p><p align=\"center\"><span style=\" font-size:14pt;\">Program: maze-gui-generator</span></p><p align=\"center\"><span style=\" font-size:14pt;\">GUI field generator for TRIK Studio simulator.</span><br/></p><p align=\"center\"><span style=\" font-size:14pt;\">Version: 1.2</span></p><p align=\"center\"><span style=\" font-size:14pt;\">Author: Lev Kozlov</span></p><p align=\"center\"><span style=\" font-size:14pt;\">Contributors: iakov, AlexStrNik</span></p><p align=\"center\"><span style=\" font-size:14pt;\">Copyright © 2020 Lev Kozlov</span><br/></p><p align=\"center\"><span style=\" font-size:14pt;\">Licence: Apache 2.0</span></p></body></html>"))
        self.InfoLabel.setText(_translate(
            "aboutWidget", "<html><head/><body><p align=\"center\">For any issues contact me on telegram: @robot_lev</p></body></html>"))
        self.telegramChannel.setText(_translate(
            "aboutWidget", "<html><head/><body><p align=\"center\">press to copy link to telegram channel: </p><p align=\"center\">https://t.me/maze_gui_gen</p></body></html>"))
        self.actionAgree.setText(_translate("aboutWidget", "Ok"))
