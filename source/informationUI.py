# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'information.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InformationWidget(object):
    def setupUi(self, InformationWidget):
        InformationWidget.setObjectName("InformationWidget")
        InformationWidget.resize(900, 600)
        InformationWidget.setMinimumSize(QtCore.QSize(900, 600))
        InformationWidget.setMaximumSize(QtCore.QSize(900, 600))
        self.tutorialImage = QtWidgets.QLabel(InformationWidget)
        self.tutorialImage.setGeometry(QtCore.QRect(0, 0, 900, 600))
        self.tutorialImage.setText("")
        self.tutorialImage.setPixmap(QtGui.QPixmap("app_screenshots/out_1.png"))
        self.tutorialImage.setScaledContents(True)
        self.tutorialImage.setObjectName("tutorialImage")
        self.b_nextImage = QtWidgets.QPushButton(InformationWidget)
        self.b_nextImage.setGeometry(QtCore.QRect(880, 240, 20, 101))
        self.b_nextImage.setObjectName("b_nextImage")
        self.b_previousImage = QtWidgets.QPushButton(InformationWidget)
        self.b_previousImage.setGeometry(QtCore.QRect(0, 240, 20, 101))
        self.b_previousImage.setObjectName("b_previousImage")

        self.retranslateUi(InformationWidget)
        QtCore.QMetaObject.connectSlotsByName(InformationWidget)

    def retranslateUi(self, InformationWidget):
        _translate = QtCore.QCoreApplication.translate
        InformationWidget.setWindowTitle(_translate("InformationWidget", "Tutorial"))
        self.b_nextImage.setText(_translate("InformationWidget", "N"))
        self.b_previousImage.setText(_translate("InformationWidget", "P"))