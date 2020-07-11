from random import randint, shuffle
import sys
sys.setrecursionlimit(50000)  
class Graph:
    def __init__(self, size_x, size_y):
        self.visited = []
        self.size_x = size_x
        self.size_y = size_y
        self.map = [[-1] * size_x * size_y for i in range(size_y * size_x)] 

    def getNextVertex(self, vertex, direction):
        next_vertex = vertex
        if direction == 0:
            next_vertex -= self.size_x if next_vertex > self.size_x else 0
        elif direction == 1:
            next_vertex += 1 if next_vertex % self.size_x != self.size_x - 1 else 0
        elif direction == 2:
            next_vertex += self.size_x if next_vertex < self.size_x * (self.size_y - 1) else 0
        elif direction == 3:
            next_vertex -= 1 if next_vertex % self.size_x != 0 else 0
        return next_vertex if next_vertex != vertex else False
    def generateGraph(self, vertex, flag = True):
        if vertex in self.visited:
            return True
        # print('entered', vertex)
        self.visited.append(vertex)
        available = []
        for d in range(4):
            n_v = self.getNextVertex(vertex, d)
            if n_v and not n_v in self.visited:
                available.append(n_v)
        if len(available) != 0:
            ways = randint(1, len(available))
            shuffle(available)
            for way in range(ways):
                selected_vertex = available[way]
                if (not flag and not selected_vertex in self.visited) or flag:
                    self.map[vertex][selected_vertex] = 1
                    self.map[selected_vertex][vertex] = 1
                    self.generateGraph(selected_vertex, flag)
                else:
                    continue
    def getMapVertexList(self):
        out = [[-1, -1, -1, -1] for vertex in range(self.size_x * self.size_y)]
        for vertex in range(self.size_x * self.size_y):
            for d in range(4):
                nv = self.getNextVertex(vertex, d)
                if nv:
                    out[vertex][d] = self.map[vertex][nv]
        # for vi, vl in enumerate(out):
        #     print(vi, vl)
        return out

# g = Graph(5, 5)
# g.generateGraph(randint(0, 24))
# v = (g.getMapVertexList())
# for vi, vl in enumerate(v):
#     print(vi, vl)