import sys


class Node:
    def __init__(self, coord, parent=None, g=0):
        self.coord = coord
        self.parent = parent
        self.visited = False
        self.f = -1
        self.g = g
        self.solution = False


class Stack:
    def __init__(self):
        self.arr = []

    def add(self, node):
        self.arr.append(node)

    def remove(self):
        if self.empty():
            raise Exception("empty stack")
        else:
            node = self.arr[-1]
            self.arr = self.arr[:-1]
            return node

    def contains(self, coord):
        return any(coord == node.coord for node in self.arr)

    def empty(self):
        return len(self.arr) == 0


class Queue(Stack):
    def remove(self):
        if self.empty():
            raise Exception("empty queue")
        else:
            node = self.arr[0]
            self.arr = self.arr[1:]
            return node


class PQueue(Queue):
    def add(self, node):
        self.arr.append(node)
        self.arr.sort(key=lambda nodes: nodes.f)    # sorts the list by lowest f value


class Maze:
    def __init__(self, filename):
        self.height = 10
        self.width = 10
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
        counter = 0
        self.arr = [[0 for x in range(self.width)] for y in range(self.height)]
        for line in lines:
            tmp = list(line.replace(" ", ""))
            tmp = [int(i) for i in tmp]
            self.arr[counter] = tmp
            counter += 1

        if self.arr[0].count(0) != 1:
            raise Exception("more than one end point")
        if self.arr[9].count(0) != 1:
            raise Exception("more than one start point")

        # finds the start and end points of the maze
        for i in range(self.width):
            if self.arr[0][i] == 0:
                self.end = (0, i)
            if self.arr[9][i] == 0:
                self.start = (9, i)

        self.explored = None
        self.solution = []
        self.solved = []

    def neighbors(self, coord):
        row, col = coord
        # spaces adjacent to coord
        adjacent = [
            (row, col - 1),
            (row - 1, col),
            (row, col + 1),
            (row + 1, col)
        ]

        valid_neighbors = []
        for (r, c) in adjacent:
            # makes sure the coordinates are valid
            if (0 <= r < self.height) and (0 <= c < self.width) and (self.arr[r][c] != 1):
                valid_neighbors.append((r, c))
        return valid_neighbors

    def DFS(self):
        start = Node(self.start, None)
        stack = Stack()
        stack.add(start)
        self.explored = set()

        while True:
            if stack.empty():
                raise Exception("no solution")

            node = stack.remove()

            if node.coord == self.end:
                path = []
                while node is not None:
                    path.insert(0, node.coord)
                    node.solution = True
                    node = node.parent
                self.solution = path
                return

            node.visited = True
            self.explored.add(node.coord)

            for coord in self.neighbors(node.coord):
                if (not stack.contains(coord)) and (coord not in self.explored):
                    child = Node(coord, node)
                    stack.add(child)

    def BFS(self):
        start = Node(self.start, None)
        queue = Queue()
        queue.add(start)
        self.explored = set()

        while True:
            if queue.empty():
                raise Exception("no solution")

            node = queue.remove()

            if node.coord == self.end:
                path = []
                while node is not None:
                    path.insert(0, node.coord)
                    node.solution = True
                    node = node.parent
                self.solution = path
                return

            node.visited = True
            self.explored.add(node.coord)

            for coord in self.neighbors(node.coord):
                if (not queue.contains(coord)) and (coord not in self.explored):
                    child = Node(coord, node)
                    queue.add(child)

    def a_star(self):
        open_list = PQueue()
        self.explored = set()

        start = Node(self.start, None, 0)
        self.solve_f(start)

        open_list.add(start)

        while not open_list.empty():
            node = open_list.remove()

            if node.coord == self.end:
                path = []
                while node is not None:
                    path.insert(0, node.coord)
                    node.solution = True
                    node = node.parent
                self.solution = path
                return

            self.explored.add(node.coord)
            for coord in self.neighbors(node.coord):
                if (not open_list.contains(coord)) and (coord not in self.explored):
                    child = Node(coord, node, node.g + 1)
                    self.solve_f(child)

                    if not open_list.contains(coord):
                        open_list.add(child)
                    elif child.f < node.f:
                        open_list.add(child)

    def solve_f(self, node):
        # solves for f(n) = g(n) + h(n)
        node.f = node.g + (abs(self.end[0] - node.coord[0]) + abs(self.end[1] - node.coord[1]))

    def print(self):
        self.solved = self.arr

        for (r, c) in self.explored:
            self.solved[r][c] = 2

        for (r, c) in self.solution:
            self.solved[r][c] = 5

        for row in self.solved:
            print(row)

    def write_solution(self, filename):
        solution = open(filename + ".txt", "w")
        for i in range(self.height):
            for j in range(self.width):
                solution.write(str(self.solved[i][j]) + " ")
            solution.write("\n")
        solution.close()


if __name__ == '__main__':
    maze = Maze(sys.argv[1])
    file = 'default'

    if 'bfs' in sys.argv:
        maze.BFS()
        file = 'bfs'
    elif 'astar' in sys.argv:
        maze.a_star()
        file = 'astar'
    else:
        maze.DFS()
        file = 'dfs'

    maze.print()
    maze.write_solution(file)
    print("Solved using " + file)

