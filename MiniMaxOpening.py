import helper
import Tree
import time

def generate_tree(board, next_turn, max_depth, generator_white, generator_black, static_estimate):

    # Create root at given board
    root = Tree.Node(board, value=None, depth=0)

    # Determine whose turn is next from current board
    current_turn = 0 if next_turn == "White" else 1

    # Generate children with DFS: Next move 0 = white, 1 = black
    generate_tree_recurse(cur_node=root,
                          current_turn=current_turn,
                          generator_white=generator_white,
                          generator_black=generator_black,
                          static_estimate=static_estimate,
                          cur_depth=1,
                          max_depth=max_depth)

    return root

def generate_tree_recurse(cur_node, current_turn, generator_white, generator_black, static_estimate, cur_depth, max_depth):

    # Base case
    if cur_depth > max_depth:
        return

    # Even if white's turn, odd if black's turn
    generator = generator_white if current_turn % 2 == 0 else generator_black
    player = "White's " if current_turn % 2 == 0 else "Black's "

    # Generate children of current node and add to children list
    children_list = generator(cur_node.board)

    for child in children_list:

        child_node = Tree.Node(child, value=static_estimate(child), depth=cur_depth) if cur_depth == max_depth \
            else Tree.Node(child, value=None, depth=cur_depth)

        cur_node.add_child(child_node)

        # print("Depth = ", child_node.depth, " ", player, "move")
        # helper.print_board(child_node.board)
        # print("Static Value= ", child_node.value, "\n")

    # Recurse on children
    for child_node in cur_node.children:
        generate_tree_recurse(child_node, current_turn + 1, generator_white, generator_black, static_estimate, cur_depth + 1, max_depth)

def minimax_game(tree):
    pass

def max_min(cur_node):
    pass

def min_max(cur_node):

    pass






pos = helper.read_file_contents()
print("Current Board")
helper.print_board(pos)
print()

start_time = time.time()

tree = generate_tree(board=pos,
                     max_depth=3,
                     next_turn="Black",
                     generator_white=helper.generate_moves_opening,
                     generator_black=helper.generate_moves_opening_black,
                     static_estimate=helper.static_estimation_opening)

end_time = time.time()
elapsed_time = end_time - start_time

print("Number of nodes: ", Tree.Node.count)
print("Elapsed time:", elapsed_time, "seconds")