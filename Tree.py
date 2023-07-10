class Node(object):
    def __init__(self, board, value):
        self.board = board
        self.value = value
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

