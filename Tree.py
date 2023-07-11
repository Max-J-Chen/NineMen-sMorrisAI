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


def generate_tree(board, max_depth, generator, static_estimate):
    # Create root at given board
    root = Node(board, value=None, depth=0)

    # Generate children with DFS: Next move 0 = white, 1 = black
    generate_tree_recurse(cur_node=root,
                          generator=generator,
                          static_estimate=static_estimate,
                          cur_depth=1,
                          max_depth=max_depth)

    return root

def generate_tree_recurse(cur_node, generator, static_estimate, cur_depth,
                          max_depth):
    # Base case
    if cur_depth > max_depth:
        return

    # Generate children of current node and add to children list
    children_list = generator(cur_node.board)

    for child in children_list:
        child_node = Node(child, value=static_estimate(child), depth=cur_depth) if cur_depth == max_depth \
            else Node(child, value=None, depth=cur_depth)

        cur_node.add_child(child_node)

    # Recurse on children
    for child_node in cur_node.children:
        generate_tree_recurse(child_node, generator, static_estimate,
                              cur_depth + 1, max_depth)
