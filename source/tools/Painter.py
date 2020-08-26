"""Module helps to draw field png preview"""

from PIL import Image, ImageDraw

class Paint:
    def __init__(self, adj_map: list, matrix: list) -> list:
        """
            The constructor for Painter class

            Parameters:
            adj_map (list): matrix: vertex -> vertices [up, right, bottom, left]
            matrix  (list): matrix with center buttons values
        """
        self.walls_map = adj_map
        self.cells_map = matrix
        self.height = len(matrix)
        self.width = len(matrix[0])
        self.const_move = 10    # outline width in pixels

    def saveMazeImage(self, path: str) -> None:
        """
            Function saves image with maze with walls at given path
        """
        size = 30
        img = self.createImage( self.width * size + self.const_move * 2,
                                self.height * size + self.const_move * 2)
        im_d = ImageDraw.Draw(img)
        for x_i in range(self.width):
            for y_i in range(self.height):
                vertex =  y_i * self.width + x_i

                # coordinates of left upper edge of cell
                x_start = x_i * size + self.const_move
                y_start = y_i * size + self.const_move

                if self.walls_map[vertex][0]:
                    self.addLine(im_d, [x_start, y_start, x_start + size, y_start])
                else:
                    self.addDottedLine(im_d, [x_start, y_start, x_start + size, y_start])

                if self.walls_map[vertex][1] and x_i == self.width - 1:
                    self.addLine(im_d, [x_start + size, y_start, x_start + size, y_start + size])
                else:
                    self.addDottedLine(im_d, [x_start + size, y_start, x_start + size, y_start + size])

                if self.walls_map[vertex][2] and y_i == self.height - 1:
                    self.addLine(im_d, [x_start, y_start + size, x_start + size, y_start + size])
                else:
                    self.addDottedLine(im_d, [x_start, y_start + size, x_start + size, y_start + size])

                if self.walls_map[vertex][3]:
                    self.addLine(im_d, [x_start, y_start, x_start, y_start + size])
                else:
                    self.addDottedLine(im_d, [x_start, y_start, x_start, y_start + size])
        
        self.showImage(img)
        img.save(path)
 
    def saveLineMazeImage(self, path: str) -> None:
        """
            Function saves images with maze with lines at given path
        """
        size = 30
        half_size = size // 2
        img = self.createImage( self.width * size + self.const_move * 2,
                                self.height * size + self.const_move * 2)
        im_d = ImageDraw.Draw(img)
        for x_i in range(self.width):
            for y_i in range(self.height):
                vertex =  y_i * self.width + x_i

                # coordinates of left upper edge of cell
                x_start = x_i * size + self.const_move + half_size
                y_start = y_i * size + self.const_move + half_size

                if not self.walls_map[vertex][0]:
                    self.addLine(im_d, [x_start, y_start, x_start, y_start - half_size])

                if not self.walls_map[vertex][1]:
                    self.addLine(im_d, [x_start, y_start, x_start + half_size, y_start])

                if not self.walls_map[vertex][2]:
                    self.addLine(im_d, [x_start, y_start, x_start, y_start + half_size])

                if not self.walls_map[vertex][3]:
                    self.addLine(im_d, [x_start, y_start, x_start - half_size, y_start])
        
        # self.showImage(img)
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
        if coors[0] == coors[2]:    # vertical line
            x = coors[0]
            for y in range(coors[1], coors[3], 3):
                image_draw.point([x, y], fill="black")
        else:   # horizontal line
            y = coors[1]
            for x in range(coors[0], coors[2], 3):
                image_draw.point([x, y], fill="black")

    def createImage(self, width: int, height: int): 
        """
            Wrapped PIL function to create an empty image with white background
            returns Image
        """
        return Image.new("RGB", (width, height), color = "white")
    
    def showImage(self, image) -> None:
        """
            Wrapped function to show image
        """
        image.show()
