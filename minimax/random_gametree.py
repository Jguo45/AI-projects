# Paul Burkhardt, Ph.D.
# November 08, 2021
#
# CMSC 471: Introduction to Artificial Intelligence
#
# Random two-player game tree generator.
#
# Nodes at each tree level represent a game state and each level is a ply,
# i.e. player turn.
#
# Each node in the tree has an ID from {0, 1} where 0 is for even levels
# starting with the zeroth level and 1 for odd levels. Thus all nodes in a level
# have the same node ID.
#
# Each leaf node is initialized by a random final game score:
#
#  1 : win
# -1 : lose
#  0 : draw
import random
from random import *
class node:
    def __init__(self, key):
        self.key = key
        self.neighbor = []
        self.id = None
        # used to determine if node was pruned
        self.visited = False

    def insert(self, key):
        self.neighbor.append(node(key))

class gametree:
    def __init__(self, branching_factor, depth):
        self.bf = branching_factor
        self.depth = depth
        self.root = node(None)
        self.root.id = 0
        self.pruned = 0
        self.nodes = 0

    def _random_insert(self, node):
        for i in range(randint(0, self.bf)):
            node.insert(None)

    def _build(self, node, k):
        if (k == self.depth):
            node.key = randint(-1, 1)
            return
        self._random_insert(node)
        if (len(node.neighbor) == 0):
            node.key = randint(-1, 1)
        for u in node.neighbor:
            u.id = (k+1) % 2
            self._build(u, k+1)
            
    def get_root(self):
        return self.root

    def generate(self):
        while (len(self.root.neighbor) == 0):
            self._build(self.root, 0)

    def print(self, node):
        for u in node.neighbor:
            self.print(u)
        print(f"key = {node.key}, id = {node.id}")

    # Minimax Algorithm
    def minimax(self, node):
        node.key = self.maxi(node, float('-inf'), float('inf'))
        # counts the number of pruned nodes
        self.count_pruned(self.root)
        return node.key

    def maxi(self, node, alpha, beta):
        node.visited = True
        # node is a leaf node, return its key
        if len(node.neighbor) == 0:
            return node.key

        node.key = float('-inf')
        # loops through every child node
        for n in node.neighbor:
            x = self.mini(n, alpha, beta)
            node.key = max(node.key, x)
            # calculates the lower bound of the max key
            alpha = max(alpha, node.key)

            # subtree can be pruned
            if beta <= alpha:
                # root node of pruned subtree is pruned as well
                node.visited = False
                break
        return node.key

    def mini(self, node, alpha, beta):
        node.visited = True
        if len(node.neighbor) == 0:
            return node.key

        node.key = float('inf')
        for n in node.neighbor:
            x = self.maxi(n, alpha, beta)
            node.key = min(node.key, x)
            beta = min(beta, node.key)

            if beta <= alpha:
                node.visited = False
                break
        return node.key

    def count_pruned(self, node):
        if not node.visited:
            self.pruned += 1
        for u in node.neighbor:
            self.count_pruned(u)

    def count_nodes(self, node):
        self.nodes += 1
        for u in node.neighbor:
            self.count_nodes(u)
