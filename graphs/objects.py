from .helpers import get_label


class Graph:
    def __init__(self):
        self._graph = {}

    def add(self, node):
        node = get_label(node)

        if self._graph.get(node) is not None:
            raise ValueError('Node labels must be unique')

        self._graph[node] = set()

    def remove(self, node):
        node = get_label(node)

        for connected_node in self._graph.get(node):
            self._graph[connected_node].remove(node)

        del self._graph[node]

    def connect(self, first_node, second_node):
        f = lambda x : get_label(x)
        first_node, second_node = f(first_node), f(second_node)

        self._graph[first_node].add(second_node)
        self._graph[second_node].add(first_node)

    def disconnect(self, first_node, second_node):
        f = lambda x : get_label(x)
        first_node, second_node = f(first_node), f(second_node)

        self._graph[first_node].discard(second_node)
        self._graph[second_node].discard(first_node)

    def __eq__(self, other):
        return self._graph == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self._graph)

    def __iter__(self):
        self._nodes = sorted(self._graph.keys())
        return self

    def __next__(self):
        try:
            return self._nodes.pop(0)
        except IndexError:
            raise StopIteration

    def __getitem__(self, node):
        node = get_label(node)
        return sorted(self._graph.__getitem__(node))

