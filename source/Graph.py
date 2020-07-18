from random import randint, shuffle
import sys
# sys.setrecursionlimit(50000)  
class Graph:
    def __init__(self, size_x, size_y):
        self.visited = []
        self.size_x = size_x
        self.size_y = size_y
        self.map = [[-1] * size_x * size_y for i in range(size_y * size_x)] 

    def getNextVertex(self, vertex, direction):
        next_vertex = vertex
        if direction == 0:
            next_vertex -= self.size_x if vertex > self.size_x - 1 else 0
        elif direction == 1:
            next_vertex += 1 if vertex % self.size_x != self.size_x - 1 else 0
        elif direction == 2:
            next_vertex += self.size_x if vertex + self.size_x < self.size_x * self.size_y else 0
        elif direction == 3:    
            next_vertex -= 1 if vertex % self.size_x != 0 else 0
        out = next_vertex if next_vertex != vertex and 0 <= next_vertex < self.size_y * self.size_y else -1
        return out

    def generateGraph(self, start_vertex, loops = True):
        self.backtrackerAlgo(start_vertex)
        if not loops:
            return loops

        walls = []

        for v1 in range(self.size_x * self.size_y):
            for v2 in range(v1 + 1, self.size_x * self.size_y):
                if self.map[v1][v2] != 1:
                    walls.append((v1, v2))

        for _ in range(len(walls) // 5):
            delete_index = randint(0, len(walls) - 1)
            v1, v2 = walls[delete_index]
            self.map[v1][v2] = 1
            self.map[v2][v1] = 1

    def backtrackerAlgo(self, start_vertex):
        queue = [start_vertex]
        visited = [start_vertex]
        while len(queue) != 0:
            current_vertex = queue[len(queue) - 1] # current is last
            directions = [0, 1, 2, 3]
            vertices = []
            for direction in directions:
                vertex = self.getNextVertex(current_vertex, direction)
                if vertex != -1 and not vertex in visited : vertices.append(vertex)
            shuffle(vertices)
            for next_vertex in vertices[:randint(1, 4)]:
                try:
                    self.map[current_vertex][next_vertex] = 1
                    self.map[next_vertex][current_vertex] = 1
                except:
                    raise ZeroDivisionError(current_vertex, next_vertex)
                visited.append(next_vertex)
                queue.append(next_vertex)
                # break
            if queue[len(queue) - 1] == current_vertex:
                queue.pop()

    def loopGraph(self, vertex, flag = True):
        if vertex in self.visited:
            return True
        # print('entered', vertex)
        self.visited.append(vertex)
        available = []
        for d in range(4):
            n_v = self.getNextVertex(vertex, d)
            # if n_v and not n_v in self.visited:
            available.append(n_v)
        if len(available) != 0:
            # ways = randint(1, len(available))
            shuffle(available)
            for way in range(4):
                selected_vertex = available[way]
                if not selected_vertex: continue
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
                if nv != -1:
                    out[vertex][d] = self.map[vertex][nv]
        return out