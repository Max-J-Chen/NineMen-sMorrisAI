from queue import Queue
import helper

black_turn_number = 0
deepest_depth = 0

class Node(object):
    count = 0

    def __init__(self, board, value, depth):
        self.board = board
        self.value = value
        self.depth = depth
        self.children = []
        self.best_child = None  # Provides a path to the best node
        Node.count += 1

    def add_child(self, obj):
        self.children.append(obj)


def generate_tree(board, max_depth, static_estimate, phase, black_turn_number_param=0):
    global black_turn_number
    global deepest_depth
    deepest_depth = 0
    black_turn_number = black_turn_number_param


    # Create root at given board
    root = Node(board, value=None, depth=0)

    # Determine which board generations to use
    if phase < 2:  # Opening phase
        first_player_gen = helper.generate_moves_opening
        second_player_gen = helper.generate_moves_opening_black

    else:  # Mid or Endgame phase
        first_player_gen = helper.generate_moves_mid
        second_player_gen = helper.generate_moves_mid_black

    # Generate children with DFS: Next move 0 = white, 1 = black
    generate_tree_recurse(cur_node=root,
                          cur_depth=1,
                          first_player_gen_phase_1=first_player_gen,
                          second_player_gen_phase_1=second_player_gen,
                          first_player_gen_phase_2=helper.generate_moves_mid,
                          second_player_gen_phase_2=helper.generate_moves_mid_black,
                          static_estimate=static_estimate,
                          max_depth=max_depth)

    return root


def generate_tree_recurse(cur_node, cur_depth,
                          first_player_gen_phase_1, second_player_gen_phase_1,
                          first_player_gen_phase_2, second_player_gen_phase_2,
                          static_estimate, max_depth):

    global black_turn_number
    global deepest_depth

    cur_depth = cur_depth

    # Base case
    if cur_depth > int(max_depth):
        return

    # Determine if Max or Min. Odd depth should be first_player_gen
    if cur_depth % 2 == 0:
        generator = second_player_gen_phase_1

        # Determine if generator is black, if so, add to black turn counter. Only matters if opening phase
        if generator == helper.generate_moves_opening_black and cur_depth > deepest_depth:
            deepest_depth = cur_depth
            black_turn_number += 1

        # Swap to mid-phase
        if black_turn_number > 7:
            generator = second_player_gen_phase_2

    else:
        generator = first_player_gen_phase_1

        # Determine if generator is black, if so, add to black turn counter. Only matters if opening phase
        if generator == helper.generate_moves_opening_black and cur_depth > deepest_depth:
            deepest_depth = cur_depth
            black_turn_number += 1

        # Swap to mid-phase
        if black_turn_number > 7:
            generator = first_player_gen_phase_2

    # Generate possible boards of current node
    possible_boards = generator(cur_node.board)

    # Current player has no more moves, then set static estimate value to inf
    if len(possible_boards) == 0:
        cur_node.value = static_estimate(cur_node.board)

    # Assign static estimation values and add to children list
    for board in possible_boards:
        if cur_depth == max_depth or board.count('x') == 0:
            child_node = Node(board, value=static_estimate(board), depth=cur_depth)
        else:
            child_node = Node(board, value=None, depth=cur_depth)

        cur_node.add_child(child_node)

    # Recurse on children
    for child_node in cur_node.children:
        generate_tree_recurse(child_node, cur_depth + 1, first_player_gen_phase_1, second_player_gen_phase_1,
                              first_player_gen_phase_2, second_player_gen_phase_2, static_estimate, max_depth)


def print_tree(root):
    queue = Queue()
    queue.put(root)
    while not queue.empty():
        cur_node = queue.get()
        helper.print_board(cur_node.board)
        print("Depth=", cur_node.depth)
        print("Static Value=", cur_node.value)
        print("Current Node= ", cur_node)
        print("Best Child Node=", cur_node.best_child)
        print("Children Nodes= ", cur_node.children, "\n")
        for child in cur_node.children:
            queue.put(child)
