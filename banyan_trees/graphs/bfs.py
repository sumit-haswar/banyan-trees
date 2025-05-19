from abc import ABC, abstractmethod
from .graph_node import GraphNode, Color
from collections import deque


class Bfs(ABC):
    def __init__(self, is_directed: bool = False):
        self.parent_of = {}
        self.is_directed = is_directed
        self.edge_count = 0

    @abstractmethod
    def pre_process_node(self, node: GraphNode):
        pass

    @abstractmethod
    def process_edge(self, source: GraphNode, sink: GraphNode):
        pass

    @abstractmethod
    def post_process_node(self, node: GraphNode):
        pass

    def bfs(self, start_node: GraphNode):
        if not start_node:
            raise TypeError

        dq = deque()
        dq.append(start_node)
        start_node.color = Color.GRAY
        self.parent_of[start_node.val] = None

        while dq:
            curr_node = dq.popleft()
            self.pre_process_node(curr_node)  # concrete method invocation
            curr_node.color = Color.BLACK  # processed

            for edge in curr_node.edges:
                # process edge if graph is directed OR sink is found for the first time
                if self.is_directed or edge.color != Color.BLACK:
                    self.process_edge(curr_node, edge)

                if edge.color == Color.WHITE:
                    edge.color = Color.GRAY  # discovered
                    self.parent_of[edge.val] = curr_node
                    dq.append(edge)

            self.post_process_node(curr_node)  # concrete method invocation
