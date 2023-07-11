import helper
import Tree
import time


def minimax_game(root):
    max_min(root)

def max_min(cur_node):
    if len(cur_node.children) == 0:
        return cur_node.value
    else:

        global positions_evaluated

        cur_node.value = float('-inf')  # set value to negative infinity
        best_child = None  # initialize best_child as None

        for child in cur_node.children:
            child_value = min_max(child)

            positions_evaluated += 1

            # print("Depth:", child.depth)
            # helper.print_board(child.board)
            # print("Static Value:", child.value, "\n")

            if child_value > cur_node.value:
                cur_node.value = child_value
                best_child = child  # update best_child if a better value is found

        cur_node.best_child = best_child  # save the best_child in the current node
        return cur_node.value


def min_max(cur_node):
    if len(cur_node.children) == 0:
        return cur_node.value
    else:

        global positions_evaluated

        cur_node.value = float('inf')  # set value to positive infinity
        best_child = None  # initialize best_child as None

        for child in cur_node.children:
            child_value = max_min(child)

            positions_evaluated += 1

            # print("Depth:", child.depth)
            # helper.print_board(child.board)
            # print("Static Value:", child.value, "\n")

            if child_value < cur_node.value:
                cur_node.value = child_value
                best_child = child  # update best_child if a better value is found

        cur_node.best_child = best_child  # save the best_child in the current node
        return cur_node.value

# def MiniMaxOpening(board, player_turn):
#     # Initialize parameters
#     positions_evaluated = 0
#     max_depth = 5
#
#     # Generate tree
#     tree = Tree.generate_tree(board=board,
#                               max_depth=max_depth,
#                               player_turn=whose_turn_is_it,
#                               generator_white=helper.generate_moves_opening,
#                               generator_black=helper.generate_moves_opening_black,
#                               static_estimate=helper.static_estimation_opening)
#
#     # Minimax
#     minimax_game(tree, whose_turn_is_it)
#
#     print("Best Move for", whose_turn_is_it)
#     helper.print_board(tree.best_child.board)
#     print("Board Position:", ''.join(map(str, tree.best_child.board)))
#     print("Positions evaluated by static estimation:", positions_evaluated)
#     print("MINIMAX estimate:", tree.value)
#     print()
#
#     return tree.best_child.board
#

# Read board
pos = helper.read_file_contents()

# Time
start_time = time.time()

# Initialize parameters
positions_evaluated = 0
max_depth = 2

# Generate tree
tree = Tree.generate_tree(board=pos,
                          max_depth=max_depth,
                          generator=helper.generate_moves_opening,
                          static_estimate=helper.static_estimation_opening)


print("Current Board")
helper.print_board(pos)
print()

minimax_game(tree)
print("Best Move for White")
helper.print_board(tree.best_child.board)
print("Board Position:", ''.join(map(str, tree.best_child.board)))
print("Positions evaluated by static estimation:", positions_evaluated)
print("MINIMAX estimate:", tree.value)
print()

end_time = time.time()
elapsed_time = end_time - start_time

print("Number of nodes generated: ", Tree.Node.count)
print("Elapsed time:", elapsed_time, "seconds")

# print("Current Board:", whose_turn_is_it, "'s turn")
# helper.print_board(pos)
# print()

current_node = tree
turn_count = 1
while current_node.best_child is not None:
    print("Turn", turn_count)
    helper.print_board(current_node.best_child.board)

    current_node = current_node.best_child
    turn_count += 1
