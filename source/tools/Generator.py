"""The module provides conversion map to XML field"""

from collections import OrderedDict
import xmltodict
import source.tools.Const as const  # pylint: disable=import-error

class FieldGenerator:
    def __init__(self, settings : dict):
        """
            The constructor for Field Generator class

            Parameters:
            x (int): field x-direction size
            y (int): field y-direction size
        """
        keys = const.FIELD_GENERATOR_SETTINGS_KEYS
        for key in keys:
            if not key in settings:
                raise Exception("There is no {} key in settings dictionary".format(key))

        self.start_id_container = []
        self.finish_id_container = []
        self.walls_id_xml = 0
        self.xml_line_width = int(settings['valueLinePixelSize']) # 6
        self.xml_line_color = int(settings['valueColorLine']) # "000000"
        self.size_x = int(settings['x']) # x
        self.size_y = int(settings['y']) # y
        self.timelimit = [int(p) for p in settings['valueExcersizeTimelimit']] # timelimit
        self.cell_size_line = int(settings['valueLineCellSize']) # -1
        self.cell_size_maze = int(settings['valueMazeCellSize']) # -1
        self.robot_id = const.ROBOTICS_KIT_TO_ID[settings['roboticsKit']]

    def getXML_line_width(self):
        return self.xml_line_width

    def getXML_line_color(self):
        return self.xml_line_color

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

    def getXML_line(self, x_start, y_start, x_len, y_len) -> OrderedDict:
        """
            Function returns OrderedDict for XML generation
            Dictionary describes one <line>, should be inside <colorFields> </colorField>
            info: https://help.trikset.com/v/en/studio/2d-model/settings#less-than-line-greater-than
            to add this dictionary in your xml field use:

            try:
                doc['root']['world']['colorFields']['line'].append(FieldGenerator.getXML_line(params))
            except TypeError:
                doc['root']['world']['colorFields'] = OrderedDict()
                doc['root']['world']['colorFields'].update([('line', [FieldGenerator.getXML_line(params)])])

            XML code example:
            <line stroke-width="6" fill-style="none" end="250:-50" id="{line1}" stroke-style="solid"
                fill="#ff000000" stroke="#ff000000" begin="50:-50"/>
        """
        width = self.getXML_line_width()    # width in pixels   (integer)
        color = self.getXML_line_color()    # color in hex      (string)
        out_dict = OrderedDict()
        out_dict.update([("@stroke-width", str(width)),
                         ("@fill-width", "none"),
                         ("@begin", str(x_start) + ":" + str(y_start)),
                         ("@end", str(x_start + x_len) + ":" + str(y_start + y_len)),
                         ("@id", "{wall" + str(self.walls_id_xml) + "}"),
                         ("@stroke-style", "solid"),
                         ("@fill", "#" + str(color)),
                         ("@stroke", "#" + str(color)
                         )])
        self.walls_id_xml += 1
        return out_dict

    def getXML_wall(self, x_start, y_start, x_len, y_len) -> OrderedDict:
        """
            Function returns OrderedDict for XML generation
            Dictionary describes one <wall>, should be inside <walls> </walls>
            info: https://help.trikset.com/v/en/studio/2d-model/settings#less-than-wall-greater-than
            For example, to add this dictionary in your xml field use:

            try:
                doc['root']['world']['walls']['wall'].append(FieldGenerator.getXML_wall(params))
            except TypeError:
                doc['root']['world']['walls'] = OrderedDict()
                doc['root']['world']['walls'].update([('wall', [FieldGenerator.getXML_wall(params)])])

            XML code example:
            <wall id="{wall1}" begin="50:-50" end="250:-50"/>
        """
        out_dict = OrderedDict()
        out_dict.update([("@id", "{wall" + str(self.walls_id_xml) + "}"),
                         ("@begin", str(x_start) + ":" + str(y_start)),
                         ("@end", str(x_start + x_len) + ":" + str(y_start + y_len))
                         ])
        self.walls_id_xml += 1
        return out_dict

    def getXML_start(self, x_start, y_start, x_len, y_len, zone_id=0) -> OrderedDict:
        """
            Function returns OrderedDict for XML generation
            Dictionary describes one start <region>, should be inside <region> </region>
            info: https://help.trikset.com/v/en/studio/2d-model/settings#less-than-region-greater-than
            For example, to add this dictionary in your XML field use:

            try:
                doc['root']['world']['regions']['region'].append(FieldGenerator.getXML_start(params))
            except TypeError:
                doc['root']['world']['regions'] = OrderedDict()
                doc['root']['world']['regions'].update([('region', [FieldGenerator.getXML_start(params)])])

            XML code example:
            <region visible="true" id="start_0" x="10" y="10" width="10" height="10"
                filled="true" textX="0" textY="0" color="#0000FF" text="Start" type="rectangle"></region>
        """
        out_dict = OrderedDict()
        out_dict.update([("@visible", "true"),
                         ("@id", "start_" + str(zone_id)),
                         ("@x", str(x_start)),
                         ("@y", str(y_start)),
                         ("@width", str(x_len)),
                         ("@height", str(y_len)),
                         ("@filled", "true"),
                         ("@textX", "0"),
                         ("@textY", "0"),
                         ("@color", "#0000FF"),
                         ("@text", "Start"),
                         ("@type", "rectangle")
                        ])
        return out_dict

    def getXML_finish(self, x_start, y_start, x_len, y_len, zone_id=0) -> OrderedDict:
        """
            Function returns OrderedDict for XML generation
            Dictionary describes one finish <region>, should be inside <region> </region>
            info: https://help.trikset.com/v/en/studio/2d-model/settings#less-than-region-greater-than
            For example, to add this dictionary in your XML field use:

            try:
                doc['root']['world']['regions']['region'].append(FieldGenerator.getXML_finish(params))
            except TypeError:
                doc['root']['world']['regions'] = OrderedDict()
                doc['root']['world']['regions'].update([('region', [FieldGenerator.getXML_finish(params)])])

            XML code example:
            <region visible="true" id="finish_0" x="10" y="10" width="10" height="10"
                filled="true" textX="0" textY="0" color="#FF0000" text="Finish" type="rectangle"></region>
        """
        out_dict = OrderedDict()
        out_dict.update([("@visible", "true"),
                         ("@id", "finish_" + str(zone_id)),
                         ("@x", str(x_start)),
                         ("@y", str(y_start)),
                         ("@width", str(x_len)),
                         ("@height", str(y_len)),
                         ("@filled", "true"),
                         ("@textX", "0"),
                         ("@textY", "0"),
                         ("@color", "#FF0000"),
                         ("@text", "Finish"),
                         ("@type", "rectangle")
                        ])
        return out_dict
    
    def getXML_warzone(self, x_start, y_start, x_len, y_len, zone_id=0) -> OrderedDict:
        """
            Function returns OrderedDict for XML generation
            Dictionary describes one warzone <region> (shows error when you enter this zone), should be inside <region> </region>
            info: https://help.trikset.com/v/en/studio/2d-model/settings#less-than-region-greater-than
            For example, to add this dictionary in your XML field use:

            try:
                doc['root']['world']['regions']['region'].append(FieldGenerator.getXML_warzone(params))
            except TypeError:
                doc['root']['world']['regions'] = OrderedDict()
                doc['root']['world']['regions'].update([('region', [FieldGenerator.getXML_warzone(params)])])

            XML code example:
            <region visible="true" id="warzone_0" x="10" y="10" width="10" height="10"
                filled="true" textX="0" textY="0" color="#FFFF00" text="Warzone" type="rectangle"></region>
        """
        out_dict = OrderedDict()
        out_dict.update([("@visible", "true"),
                         ("@id", "warzone_" + str(zone_id)),
                         ("@x", str(x_start)),
                         ("@y", str(y_start)),
                         ("@width", str(x_len)),
                         ("@height", str(y_len)),
                         ("@filled", "true"),
                         ("@textX", "0"),
                         ("@textY", "0"),
                         ("@color", "#FFFF00"),
                         ("@text", "Warzone"),
                         ("@type", "rectangle")
                        ])
        return out_dict

    def getXML_insideZone(self, zone_str, robot_id: str = "robot1") -> OrderedDict:
        """
            Function returns OrderedDict for XML generation
            Dictionary checks if robot is <inside>, should be inside <constraint> </constraint> or <conditions> </conditions>
            info: https://help.trikset.com/v/en/studio/2d-model/restrictions

            This part should be add to describe start constrain:

            inside_region = self.getXML_insideZone("start_" + str(start_id))
            try:
                doc['root']['constraints']['constraint'][0]['conditions']['inside'].append(inside_region)
            except KeyError:
                doc['root']['constraints']['constraint'][0]['conditions']['inside'] = [inside_region]
            
            To specify finish constraint use:

            inside_region = self.getXML_insideZone("finish_" + str(finish_id))
            try:
                doc['root']['constraints']['event'][0]['conditions']['conditions']['inside'].append(inside_region)
                doc['root']['constraints']['event'][1]['conditions']['conditions']['inside'].append(inside_region)
            except KeyError:
                doc['root']['constraints']['event'][0]['conditions']['conditions']['inside'] = [inside_region]
                doc['root']['constraints']['event'][1]['conditions']['conditions']['inside'] = [inside_region]

            To specify warzone constraint use:

            inside_region = self.getXML_insideZone("warzone_" + str(warzone_id))
            try:
                doc['root']['constraints']['constraint'][1]['conditions']['not'].append({'inside': inside_region})
            except AttributeError:
                doc['root']['constraints']['constraint'][1]['conditions']['not'] = [{'inside': inside_region}]

            XML code example:
            <inside regionId="start_finish" objectId="robot1"></inside>
        """
        out_dict = OrderedDict()
        out_dict.update([("@regionId", zone_str),
                         ("@objectId", robot_id)
                        ])
        return out_dict

    def updateTimelimit(self, doc: OrderedDict, time: list) -> OrderedDict:
        """
            Function updates timelimit for given doc (field)
            Time is (list)      [minutes, seconds]
            Returns doc
        """
        doc['root']['constraints']['timelimit']['@value'] = (
            (time[0] * 60 + time[1]) * 1000
        )
        return doc

    def updateRobotPosition(self, doc: OrderedDict, coordinates: list, cell_size: int) -> OrderedDict:
        """
            Function updates robot position for given doc (field)
            Params:
                doc          - xml field converted to               (OrderedDict)
                coordinates  - any start coordinate list            [y, x]
                cell_size    - size for cell denoted by settings    (int)
            Returns doc      - (OrderedDict)
        """
        y, x = coordinates
        k = cell_size // 50
        doc['root']['robots']['robot']['@id'] = self.robot_id
        doc['root']['robots']['robot']['@position'] = str(x * cell_size +
                                                          25 * (k - 1)) + ":" + str(y * cell_size + 25 * (k - 1))
        doc['root']['robots']['robot']['startPosition']['@x'] = str(
            x * cell_size + 25 * k)
        doc['root']['robots']['robot']['startPosition']['@y'] = str(
            y * cell_size + 25 * k)
        return doc

    def updateRegionsID(self, center_matrix: list) -> None:
        """
            Function updates containers for start, finish and warzones
            center_matrix is matrix describing values of center cells:
            0 - empty
            1 - start
            2 - finish
            3 - warzone
        """
        self.start_id_container = []
        self.finish_id_container = []
        self.warzones_id_container = []
        for y_index in range(self.size_y):
            for x_index in range(self.size_x):
                if center_matrix[y_index][x_index] == 1:
                    # start button
                    self.start_id_container.append([y_index, x_index])
                if center_matrix[y_index][x_index] == 2:
                    # finish button
                    self.finish_id_container.append([y_index, x_index])
                if center_matrix[y_index][x_index] == 3:
                    # warzone button
                    self.warzones_id_container.append([y_index, x_index])

    def setRegions(self, matrix: list, default_size: int) -> OrderedDict:
        """
            Function    addes start, finish, war zones to field pattern,
                        sets timelimit and robot's start position
            matrix: list - center buttons values containter (0 - empty, 1 - start, 2 - finish, 3 - warzone)
            default_size: int - size for every cell in TRIK Studio
        """
        self.updateRegionsID(matrix)
        field_template = const.FIELD_START_FINISH_STR

        doc = xmltodict.parse(field_template, process_namespaces=True)

        if len(self.finish_id_container) > 0:
            doc['root']['constraints'].update([('event', const.DICT_FINISH_PATTERN)])

        doc = self.updateTimelimit(doc, self.timelimit)

        last_start_coor = [0, 0]
        for start_id, start_coors in enumerate(self.start_id_container):
            y, x = start_coors
            start_region = self.getXML_start(
                x * default_size, y * default_size, default_size, default_size, start_id
            )

            try:
                doc['root']['world']['regions']['region'].append(start_region)
            except TypeError:
                doc['root']['world']['regions'] = OrderedDict()
                doc['root']['world']['regions'].update([('region', [start_region])])

            inside_region = self.getXML_insideZone("start_" + str(start_id))

            try:
                doc['root']['constraints']['constraint'][0]['conditions']['inside'].append(inside_region)
            except KeyError:
                doc['root']['constraints']['constraint'][0]['conditions']['inside'] = [inside_region]

            last_start_coor = start_coors

        for finish_id, finish_coors in enumerate(self.finish_id_container):
            y, x = finish_coors
            finish_region = self.getXML_finish(
                x * default_size, y * default_size, default_size, default_size, finish_id
            )

            try:
                doc['root']['world']['regions']['region'].append(finish_region)
            except TypeError:
                doc['root']['world']['regions'] = OrderedDict()
                doc['root']['world']['regions'].update([('region', [finish_region])])

            inside_region = self.getXML_insideZone("finish_" + str(finish_id))

            try:
                doc['root']['constraints']['event'][0]['conditions']['conditions']['inside'].append(inside_region)
                doc['root']['constraints']['event'][1]['conditions']['conditions']['inside'].append(inside_region)
            except KeyError:
                doc['root']['constraints']['event'][0]['conditions']['conditions']['inside'] = [inside_region]
                doc['root']['constraints']['event'][1]['conditions']['conditions']['inside'] = [inside_region]

        for warzone_id, warzone_coors in enumerate(self.warzones_id_container):
            y, x = warzone_coors
            warzone_region = self.getXML_warzone(
                x * default_size, y * default_size, default_size, default_size, warzone_id
            )

            try:
                doc['root']['world']['regions']['region'].append(warzone_region)  
            except TypeError:
                doc['root']['world']['regions'] = OrderedDict()
                doc['root']['world']['regions'].update([('region', [warzone_region])])

            inside_region = self.getXML_insideZone("warzone_" + str(warzone_id))

            try:
                doc['root']['constraints']['constraint'][1]['conditions']['not'].append({'inside': inside_region})
            except AttributeError:
                doc['root']['constraints']['constraint'][1]['conditions']['not'] = [{'inside': inside_region}]
        doc = self.updateRobotPosition(doc, last_start_coor, default_size)

        if len(self.warzones_id_container) == 0:
            doc['root']['constraints']['constraint'].pop()
        if len(self.start_id_container) == 0:
            doc['root']['constraints']['constraint'].pop(0)

        return doc
