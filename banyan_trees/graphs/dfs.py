from abc import ABC, abstractmethod
from .graph_node import GraphNode, Color, TimePair


class Dfs(ABC):
    def __init__(self, is_directed: bool = False):
        self.is_directed = is_directed
        self.time_pairs: dict[str, TimePair] = {}
        self.parent_of: dict[str, GraphNode] = {}

    @abstractmethod
    def process_node_early(self, node: GraphNode):
        pass

    @abstractmethod
    def process_node_late(self, node: GraphNode):
        pass

    @abstractmethod
    def process_edge(self, source: GraphNode, sink: GraphNode):
        pass

    def dfs(self, node: GraphNode, time: int):

        node.color = Color.GRAY
        time += 1
        self.time_pairs[node.val] = TimePair(time, None)

        self.process_node_early(node)

        for edge in node.edges:
            if edge.color == Color.WHITE:
                self.parent_of[edge.val] = node
                self.process_edge(node, edge)
                self.dfs(edge, time)
            elif edge.color != Color.BLACK:
                self.process_edge(node, edge)

        self.process_node_late(node)
        time += 1
        self.time_pairs[node.val].time_out = time

        node.color = Color.BLACK
