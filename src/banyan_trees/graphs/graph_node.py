from enum import Enum
from typing import List

class Color(Enum):
    WHITE = 0   # undiscovered
    GRAY = 1    # discovered
    BLACK = 2   # processed

class GraphNode:
    def __init__(self, val):
        self.val = val
        self.edges : List = []
        self.color: Color = Color.WHITE

    def add_edges(self, nodes: List['GraphNode']):
        for node in nodes:
            self.edges.append(node)

    def __str__(self):
        return str(self.val)
