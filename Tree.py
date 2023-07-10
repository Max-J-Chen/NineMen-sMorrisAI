class Node(object):

    count = 0

    def __init__(self, board, value, depth):
        self.board = board
        self.value = value
        self.depth = depth
        self.children = []
        Node.count += 1

    def add_child(self, obj):
        self.children.append(obj)

