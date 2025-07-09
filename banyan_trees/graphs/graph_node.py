from enum import Enum
from typing import Any, List


class Color(Enum):
    WHITE = 0  # undiscovered
    GRAY = 1  # discovered
    BLACK = 2  # processed


class TimePair:
    def __init__(self, time_in: int = None, time_out: int = None):
        self.time_in = time_in
        self.time_out = time_out


class GraphNode:
    def __init__(self, val, state: Any = None):
        self.val = val
        self.state = state
        self.edges: List["GraphNode"] = []
        self.color: Color = Color.WHITE

    def add_edges(self, nodes: List["GraphNode"]):
        for node in nodes:
            self.edges.append(node)

    def __str__(self):
        if self.state:
            return f"val:{self.val}, state:{self.state}"
        return f"val:{self.val}"
