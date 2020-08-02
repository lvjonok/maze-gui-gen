"""Module contains MazeGenApp class for main window"""

import os
import sys
from time import time
import xmltodict

from PyQt5 import QtGui, QtWidgets

import source.py_ui.screen as screen  # pylint: disable=import-error
from source.aboutWindow import AboutWindow  # pylint: disable=import-error
from source.informationWindow import \
    InformationWindow  # pylint: disable=import-error
from source.settingsWindow import \
    SettingsWindow  # pylint: disable=import-error
from source.tools.app_settings import (  # pylint: disable=import-error
    AppSettings, getMediaDirectory)
import source.tools.Graph as Graph # pylint: disable=import-error

MEDIA_DIRECTORY = getMediaDirectory()

class MazeGenApp(QtWidgets.QMainWindow, screen.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.settings = AppSettings()
        self.setMouseTracking(True)
        self.mouse_scroll_counter = 0   # uses to count scaling
        self.ui_x = 0                   # uses to move all map
        self.ui_y = 0
        self.ui_scale = 1               # initialize scale
        self.wall_size = 40             # center button size
        self.empty_part_size = 10       # distance between center buttons
        self.ui_last_x = 0
        self.ui_last_y = 0
        self.ui_last_time = time()
        self.walls_styles = {"empty": "QPushButton {background-color: #FFFFFF;}",
                             "filled": "QPushButton {background-color: #FFFF00;}"}
        self.cells_styles = {
            "empty": 'QPushButton {background-color: #FFFFFF;}',
            "start": 'QPushButton {background-color: #2d7cd6;}',
            "finish": 'QPushButton {background-color: #e86f6f;}',
        }
        self.wallsButtons = []

        self.settingsWindow = SettingsWindow()
        self.settingsWindow.hide()

        self.informationWindow = InformationWindow()
        self.informationWindow.hide()

        self.aboutWindow = AboutWindow()
        self.aboutWindow.hide()

        lang_set = self.settings.getSettings('locale_language')
        if lang_set:
            self.locale_language = lang_set
        else:
            self.locale_language = 'ru'

        self.reloadWindow()
        self.size_x = 5
        self.size_y = 5
        self.walls_id_xml = 0
        self.start_id_container = []
        self.finish_id_container = []
        self.generateWallsButtons(5, 5)
        self.displayWalls()

    def setRussian(self):
        self.settings.updateSettings('locale_language', 'ru')
        self.settings.sync()

        self.locale_language = 'ru'
        self.aboutWindow.setRussian()
        self.settingsWindow.setRussian()
        self.informationWindow.locale_language = 'ru'
        self.informationWindow.displayImage()

        self.menuFile.setTitle('Файл')
        self.actionExportXmlMaze.setText('Сохранить поле с лабиринтом \u2026')
        self.actionExportXmlLineMap.setText('Сохранить поле с линиями \u2026')
        self.actionExportAdjacencyMap.setText(
            'Сохранить матрицу смежности \u2026')

        self.menuView.setTitle('Вид')
        self.actionZoomIn.setText('Приблизить')
        self.actionZoomOut.setText('Отдалить')

        self.menuTools.setTitle('Инструменты')
        self.actionCreateMap.setText('Создать карту \u2026')
        self.actionRandomMap.setText('Случайно расставить стенки')
        self.actionFillMap.setText('Заполнить карту стенками')

        self.menuSettings.setTitle('Настройки')
        self.actionSettings.setText('Настройки \u2026')

        self.menuHelp.setTitle('Справка')
        self.actionTutorial.setText('Помощь \u2026')
        self.actionAboutApplication.setText(
            'О программе maze-gui-generator \u2026')

    def setEnglish(self):
        self.settings.updateSettings('locale_language', 'en')
        self.settings.sync()

        self.locale_language = 'en'
        self.aboutWindow.setEnglish()
        self.settingsWindow.setEnglish()
        self.informationWindow.locale_language = 'en'
        self.informationWindow.displayImage()

        self.menuFile.setTitle('File')
        self.actionExportXmlMaze.setText('Export maze map \u2026')
        self.actionExportXmlLineMap.setText('Export line map \u2026')
        self.actionExportAdjacencyMap.setText('Export adjacency matrix \u2026')

        self.menuView.setTitle('View')
        self.actionZoomIn.setText('Zoom in')
        self.actionZoomOut.setText('Zoom out')

        self.menuTools.setTitle('Tools')
        self.actionCreateMap.setText('Create a map \u2026')
        self.actionRandomMap.setText('Random this map')
        self.actionFillMap.setText('Fill this map')

        self.menuSettings.setTitle('Settings')
        self.actionSettings.setText('Preferences \u2026')

        self.menuHelp.setTitle('Help')
        self.actionTutorial.setText('Small help \u2026')
        self.actionAboutApplication.setText('About maze-gui-generator \u2026')

    def closeEvent(self, event):
        self.settingsWindow.close()
        self.informationWindow.close()
        self.aboutWindow.close()
        self.close()

    def resizeEvent(self, event):
        o_size = [event.oldSize().width(), event.oldSize().height()]
        c_size = [event.size().width(), event.size().height()]

        if abs(c_size[0] - o_size[0]) < 50 or abs(c_size[1] - o_size[1]) < 50:
            return

        min_size = 90
        window_sizes = [self.width() // (self.size_x + 1),
                        self.height() // (self.size_y + 1)]
        self.ui_scale = round((max(min(window_sizes), min_size)) / min_size)
        self.ui_x = 0
        self.ui_y = 0
        self.displayWalls()

    # clears window and adds triggers
    def reloadWindow(self):
        self.setupUi(self)

        # actions for file menu
        self.actionExportXmlMaze.triggered.connect(self.generateXML_maze)
        self.actionExportXmlLineMap.triggered.connect(self.generateXML_line)
        self.actionExportAdjacencyMap.triggered.connect(self.saveAdjMap)

        # actions for language selection
        self.actionRu.triggered.connect(self.setRussian)
        self.actionEn.triggered.connect(self.setEnglish)

        self.actionSettings.triggered.connect(self.settingsWindow.show)
        self.actionTutorial.triggered.connect(self.informationWindow.show)

        # actions for file menu
        self.actionCreateMap.triggered.connect(self.generateMap_init)
        self.actionFillMap.triggered.connect(
            lambda ch, filled=1: self.generateMap_init(filled))
        self.actionRandomMap.triggered.connect(self.randomGraph)

        # actions for view menu
        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.setMouseTracking(True)

        self.actionAboutApplication.triggered.connect(self.aboutWindow.show)

        if self.locale_language == 'ru':
            self.setRussian()
        else:
            self.setEnglish()

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.join(
            MEDIA_DIRECTORY, "ru.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRu.setIcon(icon1)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(os.path.join(
            MEDIA_DIRECTORY, "en.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEn.setIcon(icon2)

        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(os.path.join(
            MEDIA_DIRECTORY, "settings.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon3)

        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(os.path.join(
            MEDIA_DIRECTORY, "zoomin.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomIn.setIcon(icon4)

        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(os.path.join(
            MEDIA_DIRECTORY, "zoomout.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomOut.setIcon(icon5)

        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(os.path.join(
            MEDIA_DIRECTORY, "help.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTutorial.setIcon(icon6)

        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(os.path.join(
            MEDIA_DIRECTORY, "information.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAboutApplication.setIcon(icon7)

        icos = os.path.join(MEDIA_DIRECTORY, 'maze.ico')
        self.setWindowIcon(QtGui.QIcon(icos))

    def zoomIn(self):                                                        # zooms in map
        SCALE_DELTA = 0.1
        self.ui_scale += SCALE_DELTA
        self.displayWalls()

    def zoomOut(self):                                                       # zooms out map
        SCALE_DELTA = 0.1
        self.ui_scale -= SCALE_DELTA
        self.displayWalls()

    def displayWalls(self):                 # function draws window with walls from nothing
        old_scale = self.ui_scale
        self.reloadWindow()
        self.ui_scale = old_scale
        const_move = {'x': 30 + self.ui_x, 'y': 30 + self.ui_y}
        ew = round((self.wall_size + self.empty_part_size) * self.ui_scale)
        e = round(self.empty_part_size * self.ui_scale)
        w = round(self.wall_size * self.ui_scale)
        for y_index in range(self.size_y + 1):
            for x_index in range(self.size_x + 1):
                y_coor = y_index
                x_coor = x_index
                if y_coor != self.size_y:
                    left_button = QtWidgets.QPushButton(self.pool)
                    self.wallsButtons[y_coor][x_coor]['left']['core'] = left_button
                    left_button.setGeometry(screen.QtCore.QRect(
                        const_move['x'] + x_coor * ew, const_move['y'] + e + y_coor * ew, e, w))
                    left_button.setObjectName(
                        "b_" + str(y_coor) + "_" + str(x_coor) + "_left")
                    left_button.setStyleSheet(
                        self.wallsButtons[y_coor][x_coor]['left']['style'])
                    left_button.clicked.connect(
                        lambda ch, x=x_coor, y=y_coor: self.pressWall([y, x, 'left']))
                if x_coor != self.size_x:
                    up_button = QtWidgets.QPushButton(self.pool)
                    self.wallsButtons[y_coor][x_coor]['up']['core'] = up_button
                    up_button.setGeometry(screen.QtCore.QRect(
                        const_move['x'] + e + x_coor * ew, const_move['y'] + y_coor * ew, w, e))
                    up_button.setObjectName(
                        "b_" + str(y_coor) + "_" + str(x_coor) + "_up")
                    up_button.setStyleSheet(
                        self.wallsButtons[y_coor][x_coor]['up']['style'])
                    up_button.clicked.connect(
                        lambda ch, x=x_coor, y=y_coor: self.pressWall([y, x, 'up']))
                if x_coor != self.size_x and y_coor != self.size_y:
                    center_button = QtWidgets.QPushButton(
                        str(y_coor * self.size_x + x_coor), self.pool)
                    self.wallsButtons[y_coor][x_coor]['center']['core'] = center_button
                    center_button.setGeometry(screen.QtCore.QRect(
                        const_move['x'] + e + x_coor * ew, const_move['y'] + e + y_coor * ew, w, w))
                    center_button.setObjectName(
                        "b_" + str(y_coor) + "_" + str(x_coor) + "_center")
                    center_button.setStyleSheet(
                        self.wallsButtons[y_coor][x_coor]['center']['style'])
                    center_button.clicked.connect(
                        lambda ch, x=x_coor, y=y_coor: self.pressCell([y, x, 'center']))
        #print('time for loading is', time() - s_t)

    # moves all walls on given deltas
    def moveWalls(self, delta_x, delta_y):
        const_move = {'x': 30 + delta_x, 'y': 30 + delta_y}
        ew = round((self.wall_size + self.empty_part_size) *
                   self.ui_scale)     # distance between cells center
        # scaled empty size between cells
        e = round(self.empty_part_size * self.ui_scale)
        for y_index in range(self.size_y + 1):
            for x_index in range(self.size_x + 1):
                if y_index != self.size_y:
                    self.wallsButtons[y_index][x_index]['left']['core'].move(
                        const_move['x'] + x_index * ew, const_move['y'] + e + y_index * ew)
                if x_index != self.size_x:
                    self.wallsButtons[y_index][x_index]['up']['core'].move(
                        const_move['x'] + e + x_index * ew, const_move['y'] + y_index * ew)
                if x_index != self.size_x and y_index != self.size_y:
                    self.wallsButtons[y_index][x_index]['center']['core'].move(
                        const_move['x'] + e + x_index * ew, const_move['y'] + e + y_index * ew)
        #print('time for loading is', time() - s_t)

    # accepts mouse events
    def mouseMoveEvent(self, e):
        x = e.x()   # mouse x
        y = e.y()   # mouse y
        if time() - self.ui_last_time < 0.2:        # random time)
            self.ui_x += x - self.ui_last_x
            self.ui_y += y - self.ui_last_y
            self.moveWalls(self.ui_x, self.ui_y)

        self.ui_last_x = x
        self.ui_last_y = y
        self.ui_last_time = time()

    def wheelEvent(self, event):
        numDegrees = event.angleDelta().y() / 8
        numSteps = numDegrees / 15
        self.mouse_scroll_counter += numSteps
        # print(self.mouse_scroll_counter)
        if self.mouse_scroll_counter > 1:
            self.zoomIn()
            self.mouse_scroll_counter = 0
        elif self.mouse_scroll_counter < -1:
            self.zoomOut()
            self.mouse_scroll_counter = 0

    # trigger to random map
    def randomGraph(self):
        r_g = Graph.Graph(self.size_x, self.size_y)
        r_g.generateGraph(Graph.randint(
            0, self.size_x * self.size_y - 1), self.settingsWindow.getMazeCheckBox())
        _map = r_g.getMapVertexList()
        # for v in _map:
        #     print(v)
        self.setWalls(_map)

    # generates self.wallsButtons with given size
    def generateWallsButtons(self, x_len, y_len, filled=False):
        self.wallsButtons = []

        min_size = 60
        window_sizes = [self.width() // (x_len + 1),
                        self.height() // (y_len + 1)]
        self.ui_scale = (max(min(window_sizes), min_size)) / min_size

        for y_index in range(y_len + 1):
            self.wallsButtons.append([0] * (x_len + 1))
            for x_index in range(x_len + 1):
                # contains two buttons: one up, one left
                self.wallsButtons[y_index][x_index] = {}
                if y_index != y_len:
                    self.wallsButtons[y_index][x_index]['left'] = {
                        'style': self.walls_styles['empty'],
                        'name': "b_" + str(y_index) + "_" + str(x_index) + "_left",
                        'value': 0}
                    if x_index == 0 or x_index == x_len or filled:
                        self.wallsButtons[y_index][x_index]['left']['style'] = self.walls_styles['filled']
                        self.wallsButtons[y_index][x_index]['left']['value'] = 1
                if x_index != x_len:
                    self.wallsButtons[y_index][x_index]['up'] = {
                        'style': self.walls_styles['empty'],
                        'name': "b_" + str(y_index) + "_" + str(x_index) + "_up",
                        'value': 0}
                    if y_index == 0 or y_index == y_len or filled:
                        self.wallsButtons[y_index][x_index]['up']['style'] = self.walls_styles['filled']
                        self.wallsButtons[y_index][x_index]['up']['value'] = 1
                if x_index != x_len and y_index != y_len:
                    self.wallsButtons[y_index][x_index]['center'] = {
                        'style': self.walls_styles['empty'],
                        'name': "b_" + str(y_index) + "_" + str(x_index) + "_center",
                        'value': 0}

    # accepts mouse click on cell to setup start and finish positions
    def pressCell(self, coors):
        #print('pressed', coors)
        y, x, side = coors
        bs = self.wallsButtons[y][x][side]["style"]
        if bs == self.cells_styles["empty"]:
            self.wallsButtons[y][x][side]["style"] = self.cells_styles["start"]
            self.wallsButtons[y][x][side]["value"] = 1
        elif bs == self.cells_styles["start"]:
            self.wallsButtons[y][x][side]["style"] = self.cells_styles["finish"]
            self.wallsButtons[y][x][side]["value"] = 2
        elif bs == self.cells_styles["finish"]:
            self.wallsButtons[y][x][side]["style"] = self.cells_styles["empty"]
            self.wallsButtons[y][x][side]["value"] = 0
        bs = self.wallsButtons[y][x][side]["style"]
        self.wallsButtons[y][x][side]["core"].setStyleSheet(bs)

    # accepts mouse click on wall
    def pressWall(self, coors):
        y, x, side = coors
        #print('pr wall', coors)
        if self.wallsButtons[y][x][side]["style"] == self.walls_styles['empty']:
            self.wallsButtons[y][x][side]["style"] = self.walls_styles['filled']
            self.wallsButtons[y][x][side]['value'] = 1
        elif self.wallsButtons[y][x][side]["style"] == self.walls_styles['filled']:
            self.wallsButtons[y][x][side]["style"] = self.walls_styles['empty']
            self.wallsButtons[y][x][side]['value'] = 0
        self.wallsButtons[y][x][side]["core"].setStyleSheet(
            self.wallsButtons[y][x][side]["style"])

    # generates XML file with lines
    def generateXML_line(self):
        sliderLineCellValue = self.settingsWindow.getSliderLineCellSize()
        def_size = sliderLineCellValue * 50
        adj_map = self.generateAdjMap()
        doc = self.prepareField(sliderLineCellValue * 50)
        doc['root']['world']['colorFields'] = {'line': []}
        for y_i in range(self.size_y):
            for x_i in range(self.size_x):
                vertex = y_i * self.size_x + x_i
                if not adj_map[vertex][0]:
                    doc['root']['world']['colorFields']['line'].append(
                        (self.getXML_line(def_size // 2 + x_i * def_size, def_size // 2 + y_i * def_size, 0, -def_size // 2)))
                if not adj_map[vertex][1]:
                    doc['root']['world']['colorFields']['line'].append(
                        (self.getXML_line(def_size // 2 + x_i * def_size, def_size // 2 + y_i * def_size, def_size // 2, 0)))
                if not adj_map[vertex][2]:
                    doc['root']['world']['colorFields']['line'].append(
                        (self.getXML_line(def_size // 2 + x_i * def_size, def_size // 2 + y_i * def_size, 0, def_size // 2)))
                if not adj_map[vertex][3]:
                    doc['root']['world']['colorFields']['line'].append(
                        (self.getXML_line(def_size // 2 + x_i * def_size, def_size // 2 + y_i * def_size, -def_size // 2, 0)))
        # print(xmltodict.unparse(doc, pretty=True))

        if self.locale_language == 'ru':
            info_caption = 'Выберите файл для сохранения вашего поля'
        else:
            info_caption = 'Select file to save field to'

        saved_last_directory = self.settings.getSettings(
            'valueSavedLastDirectory')
        if saved_last_directory:
            dir_path = os.path.join(saved_last_directory, 'new_field.xml')
        else:
            # 0 index is needed path
            dir_path = os.path.join(sys.path[0], 'new_field.xml')

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption=info_caption,
                                                            directory=dir_path,
                                                            filter="Fields (*.xml)",
                                                            options=options)
        if fileName:
            # print(fileName)
            if fileName[::-1][0:4] != '.xml'[::-1]:
                fileName += '.xml'
            file_map = open(fileName, 'w')
            file_map.write(xmltodict.unparse(doc, pretty=True))
            file_map.close()

            # get head of a path and update as last directory
            self.settings.updateSettings(
                'valueSavedLastDirectory', os.path.split(fileName)[0])

    # generates XML file with maze
    def generateXML_maze(self):
        sliderMazeCellValue = self.settingsWindow.getSliderMazeCellSize()
        def_size = sliderMazeCellValue * 50
        adj_map = self.generateAdjMap()
        doc = self.prepareField(sliderMazeCellValue * 50)

        doc['root']['world']['walls'] = {'wall': []}
        for y_i in range(self.size_y):
            for x_i in range(self.size_x):
                vertex = y_i * self.size_x + x_i
                if adj_map[vertex][0]:
                    doc['root']['world']['walls']['wall'].append(
                        (self.getXML_wall(x_i * def_size, y_i * def_size, def_size, 0)))
                if adj_map[vertex][1]:
                    doc['root']['world']['walls']['wall'].append(
                        (self.getXML_wall(x_i * def_size + def_size, y_i * def_size, 0, def_size)))
                if adj_map[vertex][2]:
                    doc['root']['world']['walls']['wall'].append(
                        (self.getXML_wall(x_i * def_size, y_i * def_size + def_size, def_size, 0)))
                if adj_map[vertex][3]:
                    doc['root']['world']['walls']['wall'].append(
                        (self.getXML_wall(x_i * def_size, y_i * def_size, 0, def_size)))
        # print(xmltodict.unparse(doc, pretty=True))

        if self.locale_language == 'ru':
            info_caption = 'Выберите файл для сохранения вашего поля'
        else:
            info_caption = 'Select file to save field to'

        saved_last_directory = self.settings.getSettings(
            'valueSavedLastDirectory')
        if saved_last_directory:
            dir_path = os.path.join(saved_last_directory, 'new_field.xml')
        else:
            # 0 index is needed path
            dir_path = os.path.join(sys.path[0], 'new_field.xml')

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption=info_caption,
                                                            directory=dir_path,
                                                            filter="Fields (*.xml)",
                                                            options=options)
        if fileName:
            # print(fileName)
            if fileName[::-1][0:4] != '.xml'[::-1]:
                fileName += '.xml'
            file_map = open(fileName, 'w')
            file_map.write(xmltodict.unparse(doc, pretty=True))
            file_map.close()

            # get head of a path and update as last directory
            self.settings.updateSettings(
                'valueSavedLastDirectory', os.path.split(fileName)[0])

    # returns field with updated start and finish
    def prepareField(self, def_size):
        self.updateFinishStartID()
        field_template = ""
        if len(self.start_id_container) > 0 and len(self.finish_id_container) > 0:
            field_template = ef.FIELD_START_FINISH_STR
        elif len(self.start_id_container) > 0:
            field_template = ef.FIELD_START_STR
        elif len(self.finish_id_container) > 0:
            field_template = ef.FIELD_FINISH_STR
        else:
            field_template = ef.EMPTY_FIELD_STR

        doc = xmltodict.parse(field_template, process_namespaces=True)

        try:
            doc['root']['world']['regions'] = {'region': []}
        except KeyError:
            pass
        try:
            doc['root']['constraints']['constraint']['conditions']['inside'] = []
        except KeyError:
            pass
        try:
            doc['root']['constraints']['event'][1]['conditions']['inside'] = []
        except KeyError:
            pass
        try:
            min_sec = self.settingsWindow.getTimelimit()
            doc['root']['constraints']['timelimit']['@value'] = (
                min_sec[0] * 60 + min_sec[1]) * 1000
        except KeyError:
            pass
        last_start_coor = [0, 0]
        for start_id, start_coors in enumerate(self.start_id_container):
            y, x = start_coors
            doc['root']['world']['regions']['region'].append(self.getXML_start(
                x * def_size, y * def_size, def_size, def_size, start_id))
            in_s = {'@regionId': 'start_' +
                    str(start_id), '@objectId': 'robot1'}
            doc['root']['constraints']['constraint']['conditions']['inside'].append(
                in_s)
            last_start_coor = start_coors
        for finish_id, finish_coors in enumerate(self.finish_id_container):
            y, x = finish_coors
            doc['root']['world']['regions']['region'].append(self.getXML_finish(
                x * def_size, y * def_size, def_size, def_size, finish_id))
            in_s = {'@regionId': 'finish_' +
                    str(finish_id), '@objectId': 'robot1'}
            doc['root']['constraints']['event'][1]['conditions']['inside'].append(
                in_s)
        y, x = last_start_coor
        k = def_size // 50
        doc['root']['robots']['robot']['@position'] = str(x * def_size +
                                                          25 * (k - 1)) + ":" + str(y * def_size + 25 * (k - 1))
        doc['root']['robots']['robot']['startPosition']['@x'] = str(
            x * def_size + 25 * k)
        doc['root']['robots']['robot']['startPosition']['@y'] = str(
            y * def_size + 25 * k)
        return doc

    def updateFinishStartID(self):
        self.start_id_container = []
        self.finish_id_container = []
        for y_index in range(self.size_y):
            for x_index in range(self.size_x):
                if self.wallsButtons[y_index][x_index]['center']['value'] == 1:
                    # start button
                    self.start_id_container.append([y_index, x_index])
                if self.wallsButtons[y_index][x_index]['center']['value'] == 2:
                    # finish button
                    self.finish_id_container.append([y_index, x_index])

    # generates dict describing line
    def getXML_line(self, x_start, y_start, x_len, y_len):
        out_dict = {}
        out_dict['@stroke-width'] = str(
            self.settingsWindow.getSliderLinePixelSize())
        out_dict['@fill-style'] = 'none'
        out_dict['@begin'] = str(x_start) + ":" + str(y_start)
        out_dict['@end'] = str(x_start + x_len) + ":" + str(y_start + y_len)
        out_dict['@id'] = '{wall' + str(self.walls_id_xml) + '}'
        out_dict['@stroke-style'] = 'solid'
        out_dict['@fill'] = "#" + str(self.settingsWindow.colorLine)
        out_dict['@stroke'] = "#" + str(self.settingsWindow.colorLine)
        self.walls_id_xml += 1
        return out_dict

    # generates dict describing wall
    def getXML_wall(self, x_start, y_start, x_len, y_len):
        out_dict = {}
        out_dict['@id'] = "{wall" + str(self.walls_id_xml) + "}"
        out_dict['@begin'] = str(x_start) + ":" + str(y_start)
        out_dict['@end'] = str(x_start + x_len) + ":" + str(y_start + y_len)
        self.walls_id_xml += 1
        return out_dict

    # generates dict describing start rectangle
    def getXML_start(self, x_start, y_start, x_len, y_len, zone_id=0):
        out_dict = {}
        out_dict['@visible'] = "true"
        out_dict['@id'] = "start_" + str(zone_id)
        out_dict['@x'] = str(x_start)
        out_dict['@y'] = str(y_start)
        out_dict['@width'] = str(x_len)
        out_dict['@height'] = str(y_len)
        out_dict['@filled'] = 'true'
        out_dict['@textX'] = '0'
        out_dict['@textY'] = '0'
        out_dict['@color'] = '#0000FF'
        out_dict['@text'] = 'Start'
        out_dict['@type'] = 'rectangle'
        return out_dict

    def getXML_finish(self, x_start, y_start, x_len, y_len, zone_id=0):
        out_dict = {}
        out_dict['@visible'] = "true"
        out_dict['@id'] = "finish_" + str(zone_id)
        out_dict['@x'] = str(x_start)
        out_dict['@y'] = str(y_start)
        out_dict['@width'] = str(x_len)
        out_dict['@height'] = str(y_len)
        out_dict['@filled'] = 'true'
        out_dict['@textX'] = '0'
        out_dict['@textY'] = '0'
        out_dict['@color'] = '#FF0000'
        out_dict['@text'] = 'Finish'
        out_dict['@type'] = 'rectangle'
        return out_dict

    # generates map vertex->adjanced vertices from wallsButtons
    def generateAdjMap(self):
        adj_map = []  # vertex -> others 0 1 2 3
        current_vertex = 0
        for y_index in range(self.size_y):
            for x_index in range(self.size_x):
                adj_map.append([])
                adj_map[current_vertex].append(
                    self.wallsButtons[y_index][x_index]['up']['value'])
                adj_map[current_vertex].append(
                    self.wallsButtons[y_index][x_index + 1]['left']['value'])
                adj_map[current_vertex].append(
                    self.wallsButtons[y_index + 1][x_index]['up']['value'])
                adj_map[current_vertex].append(
                    self.wallsButtons[y_index][x_index]['left']['value'])
                # print(adj_map[current_vertex])
                current_vertex += 1
        self.adj_map = adj_map
        return adj_map

    # trigger to save maps to file
    def saveAdjMap(self):
        adj_map = self.generateAdjMap()

        if self.locale_language == 'ru':
            info_caption = 'Выберите файл для сохранения вашей матрицы'
        else:
            info_caption = 'Select file to save map to'

        saved_last_directory = self.settings.getSettings(
            'valueSavedLastDirectory')
        if saved_last_directory:
            dir_path = os.path.join(saved_last_directory, 'my_map.txt')
        else:
            # 0 index is needed path
            dir_path = os.path.join(sys.path[0], 'my_map.txt')

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption=info_caption,
                                                            directory=dir_path,
                                                            filter="Text Files (*.txt)",
                                                            options=options)

        if fileName:
            # print(fileName)
            if fileName[::-1][0:4] != '.txt'[::-1]:
                fileName += '.txt'
            file_map = open(fileName, 'w')
            file_map.write(
                'Map: vertex -> [upper wall, right wall, bottom wall, left wall]\n' +
                '1 if wall exists and 0 if there\'s no wall.' +
                'One line - one vertex starting from 0\n')
            for line in adj_map:
                file_map.write(str(line) + ',\n')

            file_map.write('\n\n\nMap: Simple adjacency matrix\n')
            for line in self.convertMap(adj_map):
                file_map.write(str(line) + ",\n")
            file_map.close()

            # get head of a path and update as last directory
            self.settings.updateSettings(
                'valueSavedLastDirectory', os.path.split(fileName)[0])

    # convert map from vertex-> adjanced vertices to vertex -> all vertices
    def convertMap(self, adj_map):
        am_v = self.size_x * self.size_y
        new_map = [[0] * am_v for i in range(am_v)]
        for vertex_i, adj in enumerate(adj_map):
            # print('cur v', vertex_i, adj)
            if 0 <= vertex_i - self.size_x <= am_v - 1:
                new_map[vertex_i][vertex_i - self.size_x] = 1 - adj[0]
            if 0 <= vertex_i + 1 <= am_v - 1 and vertex_i % self.size_x != self.size_x - 1:
                new_map[vertex_i][vertex_i + 1] = 1 - adj[1]
            if 0 <= vertex_i + self.size_x <= am_v - 1:
                new_map[vertex_i][vertex_i + self.size_x] = 1 - adj[2]
            if 0 <= vertex_i - 1 <= am_v - 1 and vertex_i % self.size_x != 0:
                new_map[vertex_i][vertex_i - 1] = 1 - adj[3]
        return new_map

    # trigger to create a new map
    def generateMap_init(self, flag=0):
        if flag == 0:
            if self.locale_language == 'en':
                text, ok = QtWidgets.QInputDialog.getText(
                    self, 'Create a map', 'Write map sizes separated by whitespace\n' +
                    'Current map will be erased!!!\n' +
                    'Maximum maze size is 2000 cells')
            else:
                text, ok = QtWidgets.QInputDialog.getText(
                    self, 'Создание карты', 'Введите размеры карты через пробел: "y x"\n' +
                    'Текущая карта будет обнулена!!!\n' +
                    'Максимальный размер карты ограничен 2000 клетками')
            if ok:
                try:
                    y_size, x_size = [int(dim) for dim in text.split()]
                except ValueError:
                    return False
                x_size = abs(x_size)
                y_size = abs(y_size)
                if (x_size * y_size) > 2000:
                    return False
                self.reloadWindow()
                self.size_x = x_size
                self.size_y = y_size
                self.generateWallsButtons(x_size, y_size, flag)
            else:
                return False
        elif flag == 1:
            self.setWalls([[0, 0, 0, 0]
                           for i in range(self.size_x * self.size_y)])
        self.displayWalls()

    # sets map to real walls
    def setWalls(self, mapVertexList):
        current_vertex = 0
        for y_index in range(self.size_y):
            for x_index in range(self.size_x):
                # direction 0
                if mapVertexList[current_vertex][0] != 1:       # if there is no way
                    self.wallsButtons[y_index][x_index]['up']['value'] = 1
                    self.wallsButtons[y_index][x_index]['up']["style"] = self.walls_styles['filled']
                else:                                           # way exists
                    self.wallsButtons[y_index][x_index]['up']['value'] = 0
                    self.wallsButtons[y_index][x_index]['up']["style"] = self.walls_styles['empty']
                self.wallsButtons[y_index][x_index]['up']["core"].setStyleSheet(
                    self.wallsButtons[y_index][x_index]['up']["style"])

                # direction 1
                # print(current_vertex)
                if mapVertexList[current_vertex][1] != 1:
                    # print('filled')
                    self.wallsButtons[y_index][x_index +
                                               1]['left']['value'] = 1
                    self.wallsButtons[y_index][x_index +
                                               1]['left']["style"] = self.walls_styles['filled']
                else:
                    # print('empty')
                    self.wallsButtons[y_index][x_index +
                                               1]['left']['value'] = 0
                    self.wallsButtons[y_index][x_index +
                                               1]['left']["style"] = self.walls_styles['empty']
                self.wallsButtons[y_index][x_index +
                                           1]['left']["core"].setStyleSheet(self.wallsButtons[y_index][x_index +
                                                                                                       1]['left']["style"])

                # direction 2
                if mapVertexList[current_vertex][2] != 1:
                    self.wallsButtons[y_index + 1][x_index]['up']['value'] = 1
                    self.wallsButtons[y_index +
                                      1][x_index]['up']["style"] = self.walls_styles['filled']
                else:
                    self.wallsButtons[y_index + 1][x_index]['up']['value'] = 0
                    self.wallsButtons[y_index +
                                      1][x_index]['up']["style"] = self.walls_styles['empty']
                self.wallsButtons[y_index + 1][x_index]['up']["core"].setStyleSheet(
                    self.wallsButtons[y_index + 1][x_index]['up']["style"])

                # direction 3
                if mapVertexList[current_vertex][3] != 1:
                    self.wallsButtons[y_index][x_index]['left']['value'] = 1
                    self.wallsButtons[y_index][x_index]['left']["style"] = self.walls_styles['filled']
                else:
                    self.wallsButtons[y_index][x_index]['left']['value'] = 0
                    self.wallsButtons[y_index][x_index]['left']["style"] = self.walls_styles['empty']
                self.wallsButtons[y_index][x_index]['left']["core"].setStyleSheet(
                    self.wallsButtons[y_index][x_index]['left']["style"])
                current_vertex += 1