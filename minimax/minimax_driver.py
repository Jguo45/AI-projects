# Paul Burkhardt, Ph.D.
# November 07, 2021
#
# CMSC 471: Introduction to Artificial Intelligence
#
# Homework: Run minimax on the generated random game tree and return the final
# game score of the max player (root of the tree).
#
# Use the provided random two-player game tree generator.
#
# The max player starts the game.
#
# The max and min players alternate turns with the even levels being the max ply
# and odd levels the min ply.
from random_gametree import *

# Do not modify.
#
# Generate random game tree.
seed(5)
branching_factor = 10
depth = 6

tree = gametree(branching_factor, depth)
root = tree.get_root()
tree.generate()
tree.count_nodes(root)


# Compute minimax and return the max player score.
tree.minimax(root)

# Final game score for the max player.
print(f"The max player final score: {root.key}")
print(f"The number of pruned nodes: {tree.pruned}")
print(f"Total nodes: {tree.nodes}")
