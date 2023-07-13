import sys
import helper
import Tree
import time

positions_evaluated = 0

def max_min(cur_node):
    # Iterate positions evaluated
    global positions_evaluated
    positions_evaluated += 1

    # Check if leaf
    if len(cur_node.children) == 0:
        return cur_node.value, None
    else:

        best_value = float('-inf')  # Set to negative infinity
        best_child_node = None

        # Iterate through each of the current node's children
        for child in cur_node.children:

            # Recursively call min_max on each child's children
            child_value, _ = min_max(child)

            # Get the largest value of the min_max value of the children
            if child_value > best_value:
                best_value = child_value
                best_child_node = child

        # Change current node's values and best_child
        cur_node.value = best_value
        cur_node.best_child = best_child_node

        return best_value, best_child_node


def min_max(cur_node):
    # Iterate positions evaluated
    global positions_evaluated
    positions_evaluated += 1

    # Check if leaf
    if len(cur_node.children) == 0:
        return cur_node.value, None
    else:

        best_value = float('inf')  # Set to infinity
        best_child_node = None

        # Iterate through each of the current node's children
        for child in cur_node.children:

            # Recursively call max_min on each child's children
            child_value, _ = max_min(child)

            # Get the smallest value of the max_min value of the children
            if child_value < best_value:
                best_value = child_value
                best_child_node = child

        # Change current node's values and best_child
        cur_node.value = best_value
        cur_node.best_child = best_child_node

        return best_value, best_child_node


def minimax(max_depth, phase, static_estimate, output_file_name, player_color):
    # Reinitialize parameters
    global positions_evaluated
    positions_evaluated = 0

    # Read board
    pos = helper.read_file_contents()

    # Swap if player is black
    if player_color == "Black":
        pos = helper.swap_pieces(pos)

    # Time
    start_time = time.time()

    # Generate tree
    tree = Tree.generate_tree(board=pos,
                              max_depth=int(max_depth),
                              phase=phase,
                              static_estimate=static_estimate)

    # Run minimax
    max_min(tree)

    # Swap back if player is black
    if player_color == "Black":
        pos = helper.swap_pieces(pos)

    # Print Current Board
    print("Current Board:")
    helper.print_board(pos)
    print()

    # Swap best board if player is black
    best_board = tree.best_child.board
    if player_color == "Black":
        best_board = helper.swap_pieces(tree.best_child.board)

    # Print Best Move Board
    print("Best Move for", player_color)
    helper.print_board(best_board)
    print("Board Position", ''.join(map(str, best_board)))
    print("Positions evaluated by static estimation:", positions_evaluated)
    print("MINIMAX estimate:", tree.value)
    print()

    # Calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print ancillary statistics
    print("Number of nodes generated: ", Tree.Node.count)
    print("Elapsed time:", elapsed_time, "seconds")

    # Store output
    helper.output_board_to_txt(best_board, output_file_name)

    # Print predicted turns
    print("\n________________________________________________")
    print("Predicted Turns: ")

    current_node = tree
    turn_count = 0
    while current_node is not None:

        if turn_count > max_depth:
            break

        # Swap if player is black
        if player_color == "Black":
            current_node.board = helper.swap_pieces(current_node.board)

        print("Turn", turn_count)
        helper.print_board(current_node.board)
        print("Depth=", current_node.depth)
        print("Static Value=", current_node.value)
        print("Best Child Node=", current_node.best_child, "\n")

        current_node = current_node.best_child
        turn_count += 1

