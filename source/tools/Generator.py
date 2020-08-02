"""The module provides conversion map to XML field"""

import xmltodict
import source.tools.empty_field as emptyFieldContainer  # pylint: disable=import-error
# from source.tools.Graph import convertMap # pylint: disable=import-error

class FieldGenerator:
    def __init__(self, x: int, y: int, timelimit: list):
        """
            The constructor for Field Generator class

            Parameters:
            x (int): field x-direction size
            y (int): field y-direction size
        """
        self.start_id_container = []
        self.finish_id_container = []
        self.walls_id_xml = 0
        self.xml_line_width = 6
        self.xml_line_color = "000000"
        self.size_x = x
        self.size_y = y
        self.timelimit = timelimit
        self.cell_size_line = -1
        self.cell_size_maze = -1

    def setCellSize(self, lineCell=False, mazeCell=False):
        if lineCell:
            self.cell_size_line = lineCell
        if mazeCell:
            self.cell_size_maze = mazeCell

    def setSizes(self, x, y):
        self.size_x = x
        self.size_y = y

    def setXML_line_width(self, pixels):
        self.xml_line_width = pixels

    def getXML_line_width(self):
        return self.xml_line_width

    def setXML_line_color(self, color):
        self.xml_line_color = color

    def getXML_line_color(self):
        return self.xml_line_color

    def setTimelimit(self, time):
        self.timelimit = time

    def getFieldMaze(self, adj_map: list, matrix: list) -> list:
        """
            Function creates XML dictionary with maze field

            adj_map (list): matrix: vertex -> vertices [up, right, bottom, left]
            matrix  (list): matrix with center buttons values
        """
        if self.cell_size_maze == -1:
            raise "Cant use not setted variable cell_size_maze"
        def_size = self.cell_size_maze * 50
        # matrix = convertMap(self.size_x, self.size_y, adj_map)
        doc = self.setRegions(matrix, self.cell_size_maze * 50)
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
        return doc

    def getFieldLineMaze(self, adj_map: list, matrix: list) -> list:
        """
            Function creates XML dictionary with line maze field

            adj_map (list): matrix: vertex -> vertices [up, right, bottom, left]
            matrix  (list): matrix with center buttons values
        """
        def_size = self.cell_size_line * 50
        # matrix = convertMap(self.size_x, self.size_y, adj_map)
        doc = self.setRegions(matrix, self.cell_size_line * 50)
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
        return doc

    # generates dictionary describing line
    def getXML_line(self, x_start, y_start, x_len, y_len) -> list:
        width = self.getXML_line_width()    # width in pixels   (integer)
        color = self.getXML_line_color()    # color in hex      (string)
        out_dict = {}
        out_dict['@stroke-width'] = str(width)
        out_dict['@fill-style'] = 'none'
        out_dict['@begin'] = str(x_start) + ":" + str(y_start)
        out_dict['@end'] = str(x_start + x_len) + ":" + str(y_start + y_len)
        out_dict['@id'] = '{wall' + str(self.walls_id_xml) + '}'
        out_dict['@stroke-style'] = 'solid'
        out_dict['@fill'] = "#" + str(color)
        out_dict['@stroke'] = "#" + str(color)
        self.walls_id_xml += 1
        return out_dict

    # generates dictionary describing wall
    def getXML_wall(self, x_start, y_start, x_len, y_len) -> list:
        out_dict = {}
        out_dict['@id'] = "{wall" + str(self.walls_id_xml) + "}"
        out_dict['@begin'] = str(x_start) + ":" + str(y_start)
        out_dict['@end'] = str(x_start + x_len) + ":" + str(y_start + y_len)
        self.walls_id_xml += 1
        return out_dict

    def getXML_start(self, x_start, y_start, x_len, y_len, zone_id=0) -> list:
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

    def getXML_finish(self, x_start, y_start, x_len, y_len, zone_id=0) -> list:
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

    def updateFinishStartID(self, center_matrix):
        # center_matrix is part of wallsButtons list which contains only values
        self.start_id_container = []
        self.finish_id_container = []
        for y_index in range(self.size_y):
            for x_index in range(self.size_x):
                if center_matrix[y_index][x_index] == 1:
                    # start button
                    self.start_id_container.append([y_index, x_index])
                if center_matrix[y_index][x_index] == 2:
                    # finish button
                    self.finish_id_container.append([y_index, x_index])
        # print(self.start_id_container)
        # print(self.finish_id_container)

    # addes start and finish zones on field
    def setRegions(self, matrix: list, default_size: int) -> list:
        self.updateFinishStartID(matrix)
        field_template = ""
        if len(self.start_id_container) > 0 and len(self.finish_id_container) > 0:
            field_template = emptyFieldContainer.FIELD_START_FINISH_STR
        elif len(self.start_id_container) > 0:
            field_template = emptyFieldContainer.FIELD_START_STR
        elif len(self.finish_id_container) > 0:
            field_template = emptyFieldContainer.FIELD_FINISH_STR
        else:
            field_template = emptyFieldContainer.EMPTY_FIELD_STR

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
            min_sec = self.timelimit
            doc['root']['constraints']['timelimit']['@value'] = (
                min_sec[0] * 60 + min_sec[1]) * 1000
        except KeyError:
            pass
        last_start_coor = [0, 0]
        for start_id, start_coors in enumerate(self.start_id_container):
            y, x = start_coors
            doc['root']['world']['regions']['region'].append(self.getXML_start(
                x * default_size, y * default_size, default_size, default_size, start_id))
            in_s = {'@regionId': 'start_' +
                                 str(start_id), '@objectId': 'robot1'}
            doc['root']['constraints']['constraint']['conditions']['inside'].append(
                in_s)
            last_start_coor = start_coors
        for finish_id, finish_coors in enumerate(self.finish_id_container):
            y, x = finish_coors
            doc['root']['world']['regions']['region'].append(self.getXML_finish(
                x * default_size, y * default_size, default_size, default_size, finish_id))
            in_s = {'@regionId': 'finish_' +
                                 str(finish_id), '@objectId': 'robot1'}
            doc['root']['constraints']['event'][1]['conditions']['inside'].append(
                in_s)
        y, x = last_start_coor
        k = default_size // 50
        doc['root']['robots']['robot']['@position'] = str(x * default_size +
                                                          25 * (k - 1)) + ":" + str(y * default_size + 25 * (k - 1))
        doc['root']['robots']['robot']['startPosition']['@x'] = str(
            x * default_size + 25 * k)
        doc['root']['robots']['robot']['startPosition']['@y'] = str(
            y * default_size + 25 * k)
        return doc
