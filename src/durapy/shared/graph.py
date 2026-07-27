class Edge:
    pass


class Node:
    pass


class Graph:
    def __init__(self, nodes: list[Node], edges: list[Edge]) -> None:
        self.nodes, self.edges = nodes, edges
