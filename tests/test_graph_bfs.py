import pytest
from banyan_trees.graphs.graph_node import Color, GraphNode
from banyan_trees.graphs.bfs import Bfs


class TestBfs(Bfs):
    def pre_process_node(self, node: GraphNode):
        pass

    def process_edge(self, source: GraphNode, sink: GraphNode):
        self.edge_count += 1

    def post_process_node(self, node: GraphNode):
        pass


class BipartiteBfs(Bfs):
    def __init__(self):
        super().__init__()
        self.is_bipartite = None

    def pre_process_node(self, node: GraphNode):
        pass

    def process_edge(self, source: GraphNode, sink: GraphNode):
        if source.state == sink.state:
            self.is_bipartite = False

        # sink state should be opposite of source state
        sink.state = self.complement_state(source.state)

    def post_process_node(self, node: GraphNode):
        pass

    def complement_state(self, state: str):
        return "X" if state == "Y" else "Y"


@pytest.fixture
def bfs_obj():
    return TestBfs()


@pytest.fixture
def bipartite_bfs():
    return BipartiteBfs()


@pytest.fixture
def undirected_graph():
    a = GraphNode("a")
    b = GraphNode("b")
    c = GraphNode("c")
    d = GraphNode("d")
    e = GraphNode("e")

    x = GraphNode("x")
    y = GraphNode("y")

    a.add_edges([b, c])
    b.add_edges([a, d, e])
    c.add_edges([a, e])
    d.add_edges([b, e, x])
    e.add_edges([c, b, d, y])

    return {"a": a, "b": b, "c": c, "d": d, "e": e, "x": x, "y": y}


@pytest.fixture
def undirected_bipartite_graph() -> GraphNode:
    a = GraphNode("a")
    b = GraphNode("b")
    c = GraphNode("c")
    d = GraphNode("d")
    e = GraphNode("e")
    f = GraphNode("e")
    g = GraphNode("e")

    a.add_edges([b, c, d])

    b.add_edges([a, e, f])
    c.add_edges([a, f, g])
    d.add_edges([a, g])

    e.add_edges([b])
    f.add_edges([b, c])
    g.add_edges([c, d])

    return a


@pytest.fixture
def undirected_non_bipartite_graph():
    a = GraphNode("a")
    b = GraphNode("b")
    c = GraphNode("c")
    d = GraphNode("d")
    e = GraphNode("e")
    f = GraphNode("e")
    g = GraphNode("e")

    a.add_edges([b, c, d])

    b.add_edges([a, e, f])
    c.add_edges([a, f, g])
    d.add_edges([a, g])

    e.add_edges([b])
    f.add_edges([b, c])
    g.add_edges([c, d])

    a.add_edges([e])

    return a


@pytest.fixture
def undirected_multiple_graphs(undirected_graph) -> dict:
    z = GraphNode("z")

    p = GraphNode("p")
    q = GraphNode("q")
    r = GraphNode("r")
    p.add_edges([q, r])

    multi_graphs = undirected_graph.copy()
    multi_graphs.update({"z": z, "p": p, "q": q, "r": r})
    return multi_graphs


def test_bfs_exploiting_traversal(undirected_graph, bfs_obj):
    root_node = undirected_graph["a"]
    bfs_obj.bfs(root_node)
    for key, val in undirected_graph.items():
        assert val.color == Color.BLACK


def test_bfs_parent_of(undirected_graph, bfs_obj):
    root_node = undirected_graph["a"]
    bfs_obj.bfs(root_node)
    assert bfs_obj.parent_of["a"] is None
    assert bfs_obj.parent_of["b"] is undirected_graph["a"]
    assert bfs_obj.parent_of["c"] is undirected_graph["a"]
    assert bfs_obj.parent_of["d"] is undirected_graph["b"]
    assert bfs_obj.parent_of["e"] is undirected_graph["b"]
    assert bfs_obj.parent_of["x"] is undirected_graph["d"]
    assert bfs_obj.parent_of["y"] is undirected_graph["e"]


def test_bfs_edge_count(undirected_graph, bfs_obj):
    root_node = undirected_graph["a"]
    bfs_obj.bfs(root_node)
    assert bfs_obj.edge_count == 8


# connected components
def test_bfs_connected_components(undirected_multiple_graphs, bfs_obj):
    connected_components = 0
    for val, node in undirected_multiple_graphs.items():
        if node.color == Color.WHITE:
            bfs_obj.bfs(node)
            connected_components += 1

    assert connected_components == 3


# is graph bi-partite
def test_bfs_is_bipartite(undirected_bipartite_graph, bipartite_bfs):
    undirected_bipartite_graph.state = "X"
    bipartite_bfs.bfs(undirected_bipartite_graph)
    assert bipartite_bfs.is_bipartite == True


def test_bfs_is_not_bipartite(undirected_non_bipartite_graph, bipartite_bfs):
    undirected_non_bipartite_graph.state = "X"
    bipartite_bfs.bfs(undirected_non_bipartite_graph)
    assert bipartite_bfs.is_bipartite == False
