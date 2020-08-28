"""Module helps to draw images for fields"""

import os
import xmltodict
import svgwrite
from PIL import Image, ImageDraw
from source.tools.app_settings import getMediaDirectory


class Paint:
    def __init__(self, adj_map: list, matrix: list) -> list:
        """
        The constructor for Painter class

        Class goal to create PNG images to check field, without opening TRIK Studio

        Parameters:
        adj_map (list): matrix: vertex -> vertices
        [up, right, bottom, left]
        matrix  (list): matrix with center buttons values
        """
        self.walls_map = adj_map
        self.cells_map = matrix
        self.height = len(matrix)
        self.width = len(matrix[0])
        self.const_move = 15  # outline width in pixels
        self.size = 100

    def saveMazeImage(self, path: str, robot_kit_id: str = "trikKitRobot") -> None:
        """
        Function saves image with maze with walls at given path
        """
        img = self.createImage(
            self.width * self.size + self.const_move * 2,
            self.height * self.size + self.const_move * 2,
        )
        im_d = ImageDraw.Draw(img)
        start_coors = self.addZones(im_d, self.cells_map)
        size = self.size
        for x_i in range(self.width):
            for y_i in range(self.height):
                vertex = y_i * self.width + x_i

                # coordinates of left upper edge of cell
                x_start = x_i * size + self.const_move
                y_start = y_i * size + self.const_move

                if self.walls_map[vertex][0]:
                    self.addLine(im_d, [x_start, y_start, x_start + size, y_start])
                else:
                    self.addDottedLine(
                        im_d, [x_start, y_start, x_start + size, y_start]
                    )

                if self.walls_map[vertex][1] and x_i == self.width - 1:
                    self.addLine(
                        im_d, [x_start + size, y_start, x_start + size, y_start + size]
                    )
                else:
                    self.addDottedLine(
                        im_d, [x_start + size, y_start, x_start + size, y_start + size]
                    )

                if self.walls_map[vertex][2] and y_i == self.height - 1:
                    self.addLine(
                        im_d, [x_start, y_start + size, x_start + size, y_start + size]
                    )
                else:
                    self.addDottedLine(
                        im_d, [x_start, y_start + size, x_start + size, y_start + size]
                    )

                if self.walls_map[vertex][3]:
                    self.addLine(im_d, [x_start, y_start, x_start, y_start + size])
                else:
                    self.addDottedLine(
                        im_d, [x_start, y_start, x_start, y_start + size]
                    )

        # paste robot into image
        MEDIA_DIRECTORY = getMediaDirectory()
        b_size = round(self.size * 0.6)
        im2 = Image.open(os.path.join(MEDIA_DIRECTORY, robot_kit_id + ".png")).resize(
            (b_size, b_size)
        )
        b_place = round(self.const_move + self.size * 0.2)
        img.paste(
            im2,
            (
                start_coors[0] * self.size + b_place,
                start_coors[1] * self.size + b_place,
            ),
        )
        # img.show()
        img.save(path)

    def saveLineMazeImage(self, path: str, robot_kit_id: str = "trikKitRobot") -> None:
        """
        Function saves images with maze with lines at given path
        """
        half_size = self.size // 2
        img = self.createImage(
            self.width * self.size + self.const_move * 2,
            self.height * self.size + self.const_move * 2,
        )
        im_d = ImageDraw.Draw(img)
        start_coors = self.addZones(im_d, self.cells_map)
        for x_i in range(self.width):
            for y_i in range(self.height):
                vertex = y_i * self.width + x_i

                # coordinates of left upper edge of cell
                x_start = x_i * self.size + self.const_move + half_size
                y_start = y_i * self.size + self.const_move + half_size

                if not self.walls_map[vertex][0]:
                    self.addLine(im_d, [x_start, y_start, x_start, y_start - half_size])

                if not self.walls_map[vertex][1]:
                    self.addLine(im_d, [x_start, y_start, x_start + half_size, y_start])

                if not self.walls_map[vertex][2]:
                    self.addLine(im_d, [x_start, y_start, x_start, y_start + half_size])

                if not self.walls_map[vertex][3]:
                    self.addLine(im_d, [x_start, y_start, x_start - half_size, y_start])

        # paste robot into image
        MEDIA_DIRECTORY = getMediaDirectory()
        b_size = round(self.size * 0.6)
        im2 = Image.open(os.path.join(MEDIA_DIRECTORY, robot_kit_id + ".png")).resize(
            (b_size, b_size)
        )
        b_place = round(self.const_move + self.size * 0.2)
        img.paste(
            im2,
            (
                start_coors[0] * self.size + b_place,
                start_coors[1] * self.size + b_place,
            ),
        )
        # img.show()
        img.save(path)

    def addLine(self, image_draw, coors: list):
        """
        Function appends a line described by given coors to image_draw
        image_draw - ImageDraw.Draw(image) object
        """
        image_draw.line(coors, fill="black", width=3)

    def addDottedLine(self, image_draw, coors: list):
        """
        Function appends a line with dots described by given coors to image_draw
        image_draw - ImageDraw.Draw(image) object
        """
        if coors[0] == coors[2]:  # vertical line
            x = coors[0]
            for y in range(coors[1], coors[3], 3):
                image_draw.point([x, y], fill="black")
        else:  # horizontal line
            y = coors[1]
            for x in range(coors[0], coors[2], 3):
                image_draw.point([x, y], fill="black")

    def addZones(self, image_draw, matrix: list) -> list:
        """
        Function appends rectangles with needed color to image draw
        returns list with start coordinates (indices) [x, y]
        """
        colors = ["#ffffff", "#2d7cd6", "#e86f6f", "#fff199"]
        last_coors = [0, 0]
        for y_index in range(self.height):
            for x_index in range(self.width):
                x_start = x_index * self.size + self.const_move
                y_start = y_index * self.size + self.const_move

                coors = [x_start, y_start, x_start + self.size, y_start + self.size]

                image_draw.rectangle(coors, fill=colors[matrix[y_index][x_index]])
                if matrix[y_index][x_index] == 1:
                    last_coors = [x_index, y_index]

        return last_coors

    def createImage(self, width: int, height: int) -> Image.Image:
        """
        Wrapped PIL function to create an empty image with white background
        returns Image
        """
        return Image.new("RGB", (width, height), color="white")

    def showImage(self, image) -> None:
        """
        Wrapped function to show image
        """
        image.show()


class SVG:
    def __init__(self, adj_map: list, matrix: list) -> list:
        """
        The constructor for SVG class

        Class goal to create SVG field image for maze with lines

        Parameters:
        adj_map (list): matrix: vertex -> vertices
        [up, right, bottom, left]
        matrix  (list): matrix with center buttons values
        """
        self.walls_map = adj_map
        self.cells_map = matrix
        self.heigth = len(matrix)
        self.width = len(matrix[0])

    def saveField(
        self, field_path: str, cell_size: int, line_color: str, line_width: int
    ) -> None:
        """
        Function creates needed SVG field and saves to given field_path
        """
        svg = svgwrite.Drawing(
            field_path,
            (self.width * cell_size, self.heigth * cell_size),
            profile="tiny",
        )
        for y_index in range(self.heigth):
            for x_index in range(self.width):
                vertex = y_index * self.width + x_index
                x_start = x_index * cell_size + cell_size // 2
                y_start = y_index * cell_size + cell_size // 2

                bcoors = [x_start, y_start]

                if not self.walls_map[vertex][0]:
                    coors = bcoors[:]
                    coors[1] += line_width // 2
                    svg.add(
                        self.createLine(
                            svg,
                            coors + [x_start, y_start - cell_size // 2],
                            line_color,
                            line_width,
                        )
                    )
                if not self.walls_map[vertex][1]:
                    coors = bcoors[:]
                    coors[0] -= line_width // 2
                    svg.add(
                        self.createLine(
                            svg,
                            coors + [x_start + cell_size // 2, y_start],
                            line_color,
                            line_width,
                        )
                    )
                if not self.walls_map[vertex][2]:
                    coors = bcoors[:]
                    coors[1] -= line_width // 2
                    svg.add(
                        self.createLine(
                            svg,
                            coors + [x_start, y_start + cell_size // 2],
                            line_color,
                            line_width,
                        )
                    )
                if not self.walls_map[vertex][3]:
                    coors = bcoors[:]
                    coors[0] += line_width // 2
                    svg.add(
                        self.createLine(
                            svg,
                            coors + [x_start - cell_size // 2, y_start],
                            line_color,
                            line_width,
                        )
                    )
        svg.save(pretty=True, indent=4)

    def createLine(self, svg, coors: list, color: str, width: int) -> None:
        """
        Wrapped svgwrite function that creates Line Object
        coors = [x1, y1, x2, y2]
        color = hex string, for example #0023FF
        width = (int) line width in pixels
        """
        start = tuple(coors[0:2])
        finish = tuple(coors[2:4])

        rgb_color = self.convertColor(color)
        svg_color = svgwrite.rgb(rgb_color[0], rgb_color[1], rgb_color[2], "%")
        return svg.line(start, finish, stroke=svg_color, stroke_width=width)

    def convertColor(self, color: str) -> list:
        """
        Function converts hex color representation to RGB list with 3 values
        """
        color = color.lstrip("#")
        hlen = len(color)
        return list(
            int(color[i : i + hlen // 3], 16) for i in range(0, hlen, hlen // 3)
        )
