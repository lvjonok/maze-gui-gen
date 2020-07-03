import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import source.screen as screen # Это наш конвертированный файл дизайна
import source.settingsUI as settingsUI
import source.empty_field as ef
import source.informationUI as informationUI
from time import sleep, time
import xmltodict, pprint, json
import source.Graph as Graph
from pathlib import Path
import collections

class InformationWindow(QtWidgets.QWidget, informationUI.Ui_InformationWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class SettingsWindow(QtWidgets.QWidget, settingsUI.Ui_settingsForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lineColorLineEdit.textEdited.connect(self.controlColor) 
        self.lineColorLineEdit.setInputMask("HHHHHH")
        self.colorLine = "#000000"
    def getSliderMaze(self) -> int:
        return self.mazeSlider.value()
    def getSliderLine(self) -> int:
        return self.lineSlider.value()
    def controlColor(self):
        text_in = self.lineColorLineEdit.text()
        self.colorLabel.setStyleSheet('QLabel {border: 3px solid blue;background-color: #'+str(text_in)+';}')
        self.colorLine = "#"+str(text_in)

class MazeGenApp(QtWidgets.QMainWindow, screen.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.mouse_scroll_counter = 0 # shoud be in range [-5, 5] if hits abs(6), zoom map
        self.ui_x = 0
        self.ui_y = 0
        self.ui_scale = 1
        self.wall_size = 40
        self.empty_part_size = 10
        self.ui_last_x = 0
        self.ui_last_y = 0
        self.ui_last_time = time()
        self.walls_styles = {   "empty":'QPushButton {background-color: #FFFFFF;}',
                                'filled':'QPushButton {background-color: #FFFF00;}'}
        self.cells_styles = {
                                "empty":'QPushButton {background-color: #FFFFFF;}',
                                "start":'QPushButton {background-color: #2d7cd6;}',
                                "finish":'QPushButton {background-color: #e86f6f;}',
        }
        self.wallsButtons = []
        self.settingsWindow = SettingsWindow()
        self.settingsWindow.hide()
        self.informationWindow = InformationWindow()
        self.informationWindow.hide()
        self.reloadWindow()
        self.size_x = 5
        self.size_y = 5
        self.walls_id_xml = 0
        self.start_id_container = []
        self.finish_id_container = []
        self.generateWallsButtons(5, 5)
        self.displayWalls(0, 0, 0)
    def reloadWindow(self):                                                     # clears window and adds triggers
        # self.ui_x = 0
        # self.ui_y = 0
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.actioncreate_map.triggered.connect(self.generateMap_init)
        self.actionexport_xml_maze.triggered.connect(self.generateXML_maze)
        self.actionexport_xml_line_map.triggered.connect(self.generateXML_line)
        self.actionexport_adjacency_map.triggered.connect(self.saveAdjMap)
        self.actionsettings.triggered.connect(self.settingsWindow.show)
        self.actioninformation.triggered.connect(self.informationWindow.show)
        self.actionfill_this_map.triggered.connect(lambda ch, flag=1 : self.generateMap_init(flag))
        self.actionrandom_this_map.triggered.connect(self.randomGraph)
        self.shortcut_in_pl = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl++'), self.pool)
        self.shortcut_in_eq = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+='), self.pool)
        self.shortcut_in_pl.activated.connect(self.zoomIn)
        self.shortcut_in_eq.activated.connect(self.zoomIn)
        self.shortcut_out = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+-'), self.pool)
        self.shortcut_out.activated.connect(self.zoomOut)
        self.setMouseTracking(True)
    def zoomIn(self, scale_delta = 0.1):                                                           # zooms in map
        self.ui_scale += scale_delta
        self.displayWalls()
    def zoomOut(self, scale_delta = 0.1):                                                          # zooms out map
        self.ui_scale -= scale_delta
        self.displayWalls()
    def displayWalls(self, delta_x = 0, delta_y = 0, zoom = 0):                 # function draws window with walls from nothing
        s_t = time()    
        self.reloadWindow()
        const_move = {'x': 30 + self.ui_x, 'y': 30 + self.ui_y}
        ew = (self.wall_size + self.empty_part_size) * self.ui_scale
        e = self.empty_part_size * self.ui_scale
        w = self.wall_size * self.ui_scale
        for y_index in range(self.size_y + 1):
            for x_index in range(self.size_x + 1):
                if y_index != self.size_y:
                    left_button = QtWidgets.QPushButton(self.pool)
                    self.wallsButtons[y_index][x_index]['left']['core'] = left_button
                    left_button.setGeometry(screen.QtCore.QRect(const_move['x'] + x_index * ew, const_move['y'] + e + y_index * ew, e, w))
                    left_button.setObjectName("b_" + str(y_index) + "_" + str(x_index) + "_left")
                    left_button.setStyleSheet(self.wallsButtons[y_index][x_index]['left']['style'])
                    left_button.clicked.connect(lambda ch, coors=[y_index, x_index, "left"] : self.pressWall(coors))
                if x_index != self.size_x:
                    up_button = QtWidgets.QPushButton(self.pool)
                    self.wallsButtons[y_index][x_index]['up']['core'] = up_button
                    up_button.setGeometry(screen.QtCore.QRect(const_move['x'] + e + x_index * ew,const_move['y'] + y_index * ew, w, e))
                    up_button.setObjectName("b_" + str(y_index) + "_" + str(x_index) + "_up")
                    up_button.setStyleSheet(self.wallsButtons[y_index][x_index]['up']['style'])
                    up_button.clicked.connect(lambda ch, coors=[y_index, x_index, "up"] : self.pressWall(coors))
                if x_index != self.size_x and y_index != self.size_y:
                    center_button = QtWidgets.QPushButton(  str(y_index * self.size_x + x_index),self.pool)
                    self.wallsButtons[y_index][x_index]['center']['core'] = center_button
                    center_button.setGeometry(screen.QtCore.QRect(const_move['x'] + e + x_index * ew, const_move['y'] + e + y_index * ew, w, w))
                    center_button.setObjectName("b_" + str(y_index) + "_" + str(x_index) + "_center")
                    center_button.setStyleSheet(self.wallsButtons[y_index][x_index]['center']['style'])
                    center_button.clicked.connect(lambda ch, coors=[y_index, x_index, "center"]: self.pressCell(coors))
        print('time for loading is', time() - s_t)
    def moveWalls(self, delta_x, delta_y, zoom = 0):                            # moves all walls on given deltas
        s_t = time()
        const_move = {'x': 30 + delta_x, 'y': 30 + delta_y}
        ew = (self.wall_size + self.empty_part_size) * self.ui_scale
        e = self.empty_part_size * self.ui_scale
        w = self.wall_size * self.ui_scale
        for y_index in range(self.size_y + 1):
            for x_index in range(self.size_x + 1):
                if y_index != self.size_y:
                    self.wallsButtons[y_index][x_index]['left']['core'].move(const_move['x'] + x_index * ew, const_move['y'] + e + y_index * ew)
                if x_index != self.size_x:
                    self.wallsButtons[y_index][x_index]['up']['core'].move(const_move['x'] + e + x_index * ew,const_move['y'] + y_index * ew)
                if x_index != self.size_x and y_index != self.size_y:
                    self.wallsButtons[y_index][x_index]['center']['core'].move(const_move['x'] + e + x_index * ew, const_move['y'] + e + y_index * ew)
        print('time for loading is', time() - s_t)      
    def mouseMoveEvent(self, e):                                                # accepts mouse events
        x = e.x()   # mouse x
        y = e.y()   # mouse y
        if time() - self.ui_last_time < 0.2:        # random time)
            self.ui_x += x - self.ui_last_x
            self.ui_y += y - self.ui_last_y
            self.moveWalls(self.ui_x, self.ui_y, 0)

        self.ui_last_x = x
        self.ui_last_y = y
        self.ui_last_time = time()
    def wheelEvent(self, event):
        numDegrees = event.angleDelta().y() / 8
        numSteps = numDegrees / 15
        self.mouse_scroll_counter += numSteps
        print(self.mouse_scroll_counter)
        if self.mouse_scroll_counter > 2:
            self.zoomIn()
            self.mouse_scroll_counter = 0
        elif self.mouse_scroll_counter < -2:
            self.zoomOut()
            self.mouse_scroll_counter = 0        
    def randomGraph(self):                                                      # trigger to random map
        r_g = Graph.Graph(self.size_x, self.size_y)
        r_g.generateGraph(Graph.randint(0, self.size_x * self.size_y))
        self.setWalls(r_g.getMapVertexList())
    def generateWallsButtons(self, x_len, y_len, filled = False):               # generates self.wallsButtons with given size
        self.wallsButtons = []
        for y_index in range(y_len + 1):
            self.wallsButtons.append([0] * (x_len + 1))
            for x_index in range(x_len + 1):
                self.wallsButtons[y_index][x_index] = {} # contains two buttons: one up, one left
                if y_index != y_len:
                    self.wallsButtons[y_index][x_index]['left'] = { 'style' : self.walls_styles['empty'],
                                                                    'name' : "b_" + str(y_index) + "_" + str(x_index) + "_left",
                                                                    'value' : 0}
                    if x_index == 0 or x_index == x_len or filled:
                        self.wallsButtons[y_index][x_index]['left']['style'] = self.walls_styles['filled']
                        self.wallsButtons[y_index][x_index]['left']['value'] = 1
                if x_index != x_len:
                    self.wallsButtons[y_index][x_index]['up'] = {   'style' : self.walls_styles['empty'],
                                                                    'name' : "b_" + str(y_index) + "_" + str(x_index) + "_up",
                                                                    'value' : 0}
                    if y_index == 0 or y_index == y_len or filled:
                        self.wallsButtons[y_index][x_index]['up']['style'] = self.walls_styles['filled']
                        self.wallsButtons[y_index][x_index]['up']['value'] = 1
                if x_index != x_len and y_index != y_len:
                    self.wallsButtons[y_index][x_index]['center'] = {   'style' : self.walls_styles['empty'],
                                                                        'name' : "b_" + str(y_index) + "_" + str(x_index) + "_center",
                                                                        'value' : 0}
    def pressCell(self,coors):                                                  # accepts mouse click on cell to setup start and finish positions
        print('pressed', coors)
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
        pass                                                            
    def pressWall(self,coors):                                                  # accepts mouse click on wall
        y, x, side = coors
        if self.wallsButtons[y][x][side]["style"] == self.walls_styles['empty']:
            self.wallsButtons[y][x][side]["style"] = self.walls_styles['filled']
            self.wallsButtons[y][x][side]['value'] = 1
        elif self.wallsButtons[y][x][side]["style"] == self.walls_styles['filled']:
            self.wallsButtons[y][x][side]["style"] = self.walls_styles['empty']
            self.wallsButtons[y][x][side]['value'] = 0
        self.wallsButtons[y][x][side]["core"].setStyleSheet(self.wallsButtons[y][x][side]["style"])
    def generateXML_line(self):                                                 # generates XML file with lines
        def_size = self.settingsWindow.getSliderLine() * 50
        adj_map = self.generateAdjMap()
        # empty_field_file = Path("source/fields/empty_field.xml")
        doc = self.prepareField(self.settingsWindow.getSliderLine() * 50)
        doc['root']['world']['colorFields'] = {'line':[]}
        for y_i in range(self.size_y):
            for x_i in range(self.size_x):
                vertex = y_i * self.size_x + x_i
                if not adj_map[vertex][0]:
                    doc['root']['world']['colorFields']['line'].append((self.getXML_line(def_size // 2 + x_i * def_size, def_size//2 + y_i * def_size, 0, -def_size//2)))
                if not adj_map[vertex][1]:
                    doc['root']['world']['colorFields']['line'].append((self.getXML_line(def_size // 2 + x_i * def_size, def_size//2 + y_i * def_size, def_size//2, 0)))
                if not adj_map[vertex][2]:
                    doc['root']['world']['colorFields']['line'].append((self.getXML_line(def_size // 2 + x_i * def_size, def_size//2 + y_i * def_size, 0, def_size//2)))
                if not adj_map[vertex][3]:
                     doc['root']['world']['colorFields']['line'].append((self.getXML_line(def_size // 2 + x_i * def_size, def_size//2 + y_i * def_size, -def_size//2, 0)))
        # print(xmltodict.unparse(doc, pretty=True))
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Select a place to save your xml file","new_field","Fields (*.xml)", options=options)

        if fileName:
            print(fileName)
            file_map = open(fileName, 'w')
            file_map.write(xmltodict.unparse(doc, pretty=True))
            file_map.close()
        pass
    def generateXML_maze(self):                                                 # generates XML file with maze
        def_size = self.settingsWindow.getSliderMaze() * 50
        adj_map = self.generateAdjMap()
        # empty_field_file = Path("source/fields/empty_field.xml")
        
        doc = self.prepareField(self.settingsWindow.getSliderMaze() * 50)
        
        doc['root']['world']['walls'] = {'wall':[]}
        for y_i in range(self.size_y):
            for x_i in range(self.size_x):
                vertex = y_i * self.size_x + x_i
                if adj_map[vertex][0]:
                    doc['root']['world']['walls']['wall'].append((self.getXML_wall(x_i * def_size, y_i * def_size, def_size, 0)))
                if adj_map[vertex][1]:
                    doc['root']['world']['walls']['wall'].append((self.getXML_wall(x_i * def_size + def_size, y_i * def_size, 0, def_size)))
                if adj_map[vertex][2]:
                    doc['root']['world']['walls']['wall'].append((self.getXML_wall(x_i * def_size, y_i * def_size + def_size, def_size, 0)))
                if adj_map[vertex][3]:
                     doc['root']['world']['walls']['wall'].append((self.getXML_wall(x_i * def_size, y_i * def_size, 0, def_size)))
        # print(xmltodict.unparse(doc, pretty=True))
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Select a place to save your xml file","new_field","Fields (*.xml)", options=options)
        if fileName:
            print(fileName)
            file_map = open(fileName, 'w')
            file_map.write(xmltodict.unparse(doc, pretty=True))
            file_map.close()
        pass
    def prepareField(self, def_size):                                                     # returns field with updated start and finish
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
            doc['root']['world']['regions'] = {'region':[]}
        except:
            pass
        try:
            doc['root']['constraints']['constraint']['conditions']['inside'] = []
        except:
            pass
        try:
            doc['root']['constraints']['event'][1]['conditions']['inside'] = []
        except:
            pass
        last_start_coor = [0, 0]
        for start_id, start_coors in enumerate(self.start_id_container):
            y, x = start_coors
            doc['root']['world']['regions']['region'].append(self.getXML_start(x * def_size, y * def_size, def_size, def_size, start_id))
            in_s = {'@regionId':'start_'+str(start_id), '@objectId':'robot1'}
            doc['root']['constraints']['constraint']['conditions']['inside'].append(in_s)
            last_start_coor = start_coors
        for finish_id, finish_coors in enumerate(self.finish_id_container):
            y, x = finish_coors
            doc['root']['world']['regions']['region'].append(self.getXML_finish(x * def_size, y * def_size, def_size, def_size, finish_id))
            in_s = {'@regionId':'finish_'+str(finish_id), '@objectId':'robot1'}
            doc['root']['constraints']['event'][1]['conditions']['inside'].append(in_s)
        y, x = last_start_coor
        k = def_size // 50
        disp = def_size // k
        doc['root']['robots']['robot']['@position'] = str(x * def_size + 25 * (k-1))+":"+str(y * def_size + 25 * (k-1))
        doc['root']['robots']['robot']['startPosition']['@x'] = str(x * def_size + 25 * k)
        doc['root']['robots']['robot']['startPosition']['@y'] = str(y * def_size + 25 * k)
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
    def getXML_line(self, x_start, y_start, x_len, y_len):                      # generates dict describing line
        out_dict = {}
        out_dict['@stroke-width'] = '6'
        out_dict['@fill-style'] = 'none'
        out_dict['@begin'] = str(x_start) + ":" + str(y_start)
        out_dict['@end'] = str(x_start + x_len) + ":" + str(y_start + y_len)
        out_dict['@id'] = '{wall'+str(self.walls_id_xml)+'}'
        out_dict['@stroke-style'] = 'solid'
        out_dict['@fill'] = str(self.settingsWindow.colorLine)
        out_dict['@stroke'] = str(self.settingsWindow.colorLine)
        self.walls_id_xml+=1
        return out_dict
    def getXML_wall(self, x_start, y_start, x_len, y_len):                      # generates dict describing wall
        out_dict = {}
        out_dict['@id'] = "{wall" + str(self.walls_id_xml) + "}"
        out_dict['@begin'] = str(x_start) + ":" + str(y_start)
        out_dict['@end'] = str(x_start + x_len) + ":" + str(y_start + y_len)
        self.walls_id_xml+= 1
        return out_dict
    def getXML_start(self, x_start, y_start, x_len, y_len, id=0):               # generates dict describing start rectangle
        out_dict = {}
        out_dict['@visible'] = "true"
        out_dict['@id'] = "start_" + str(id)
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
    def getXML_finish(self, x_start, y_start, x_len, y_len, id=0):
        out_dict = {}
        out_dict['@visible'] = "true"
        out_dict['@id'] = "finish_" + str(id)
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
    def generateAdjMap(self):                                                   # generates map vertex->adjanced vertices from wallsButtons
        adj_map = [] # vertex -> others 0 1 2 3
        current_vertex = 0
        for y_index in range(self.size_y):
            for x_index in range(self.size_x):
                adj_map.append([])
                adj_map[current_vertex].append(self.wallsButtons[y_index][x_index]['up']['value'])
                adj_map[current_vertex].append(self.wallsButtons[y_index][x_index + 1]['left']['value'])
                adj_map[current_vertex].append(self.wallsButtons[y_index + 1][x_index]['up']['value'])
                adj_map[current_vertex].append(self.wallsButtons[y_index][x_index]['left']['value'])
                print(adj_map[current_vertex])
                current_vertex += 1
                # input()
        self.adj_map = adj_map
        return adj_map
    def saveAdjMap(self):                                                       # trigger to save maps to file 
        adj_map = self.generateAdjMap()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Select a place to save txt file","my_map","Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
            file_map = open(fileName, 'w')
            file_map.write('Map: vertex -> [upper wall, right wall, bottom wall, left wall]\n1 if wall exists and 0 if there\'s no wall.\nOne line - one vertex starting from 0\n')
            for line in adj_map:
                file_map.write(str(line) + '\n')

            file_map.write('\n\n\nMap: Simple adjacency map\n')
            for line in self.convertMap(adj_map):
                file_map.write(str(line) + "\n")
            file_map.close()
        pass
    def convertMap(self, adj_map):                                              # convert map from vertex-> adjanced vertices to vertex -> all vertices
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
    def generateMap_init(self, flag = 0):                                       # trigger to create a new map
        if flag == 0:
            text, ok = QtWidgets.QInputDialog.getText(self, 'gen map', 'Write map sizes separated by whitespace\nCurrent map will be erased!!!')
            if ok:
                try:
                    y_size, x_size = [int(dim) for dim in text.split()]
                except:
                    return
                self.reloadWindow()
                self.size_x = x_size
                self.size_y = y_size
                self.generateWallsButtons(x_size, y_size, flag)
            else:
                return False
            pass
        elif flag == 1:
            self.reloadWindow()
            self.generateWallsButtons(self.size_x, self.size_y, flag)
        self.displayWalls()
    def setWalls(self, mapVertexList):                                          # sets map to real walls
        current_vertex = 0
        for y_index in range(self.size_y):
            for x_index in range(self.size_x):
                # direction 0
                if mapVertexList[current_vertex][0] != 1:
                    self.wallsButtons[y_index][x_index]['up']['value'] = 1
                    self.wallsButtons[y_index][x_index]['up']["style"] = self.walls_styles['filled']
                else:
                    self.wallsButtons[y_index][x_index]['up']['value'] = 0
                    self.wallsButtons[y_index][x_index]['up']["style"] = self.walls_styles['empty']
                self.wallsButtons[y_index][x_index]['up']["core"].setStyleSheet(self.wallsButtons[y_index][x_index]['up']["style"])
                if mapVertexList[current_vertex][1] != 1:
                    self.wallsButtons[y_index][x_index + 1]['left']['value'] = 1
                    self.wallsButtons[y_index][x_index + 1]['left']["style"] = self.walls_styles['filled']
                else:
                    self.wallsButtons[y_index][x_index + 1]['left']['value'] = 0
                    self.wallsButtons[y_index][x_index + 1]['left']["style"] = self.walls_styles['empty']
                self.wallsButtons[y_index][x_index + 1]['left']["core"].setStyleSheet(self.wallsButtons[y_index][x_index + 1]['left']["style"])
                if mapVertexList[current_vertex][2] != 1:
                    self.wallsButtons[y_index + 1][x_index]['up']['value'] = 1
                    self.wallsButtons[y_index + 1][x_index]['up']["style"] = self.walls_styles['filled']
                else:
                    self.wallsButtons[y_index + 1][x_index]['up']['value'] = 0
                    self.wallsButtons[y_index + 1][x_index]['up']["style"] = self.walls_styles['empty']
                self.wallsButtons[y_index + 1][x_index]['up']["core"].setStyleSheet(self.wallsButtons[y_index + 1][x_index]['up']["style"])
                if mapVertexList[current_vertex][3] != 1:
                    self.wallsButtons[y_index][x_index]['left']['value'] = 1
                    self.wallsButtons[y_index][x_index]['left']["style"] = self.walls_styles['filled']
                else:
                    self.wallsButtons[y_index][x_index]['left']['value'] = 0
                    self.wallsButtons[y_index][x_index]['left']["style"] = self.walls_styles['empty']
                self.wallsButtons[y_index][x_index]['left']["core"].setStyleSheet(self.wallsButtons[y_index][x_index]['left']["style"])
                current_vertex += 1

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setStyle('fusion')
    window = MazeGenApp()  # Создаём объект класса MazeGenApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()