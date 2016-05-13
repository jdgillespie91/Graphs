from functools import total_ordering


class Graph:
    def __init__(self):
        self._graph = {}

    def add(self, node):
        if self._graph.get(node) is not None:
            raise ValueError('Node labels must be unique')
        self._graph[node] = set()

    def remove(self, node):
        for connected_node in self._graph.get(node):
            self._graph[connected_node].remove(node)
        del self._graph[node]

    def connect(self, first_node, second_node):
        self._graph[first_node].add(second_node)
        self._graph[second_node].add(first_node)

    def disconnect(self, first_node, second_node):
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
        return sorted(self._graph.__getitem__(node))

    def __bool__(self):
        return bool(self._graph)


class Tree:
    def __init__(self, node=None):
        self._graph = Graph()
        if node:
            self.insert(node)

    def _add(self, node):
        self._graph.add(node)

    def _connect(self, first_node, second_node):
        self._graph.connect(first_node, second_node)

    def insert(self, node):
        pass

    def __eq__(self, other):
        return self._graph.__eq__(other)

    def __ne__(self, other):
        return self._graph.__ne__(other)

    def __repr__(self):
        return self._graph.__repr__()


@total_ordering
class Node:
    def __init__(self, label):
        self._label = label

    @property
    def label(self):
        return self._label

    def __eq__(self, other):
        if not isinstance(other, Node):
            raise TypeError('Only Node types can be compared')
        return self.label.__eq__(other.label)

    def __lt__(self, other):
        if not isinstance(other, Node):
            raise TypeError('Only Node types can be compared')
        return self.label.__lt__(other.label)

    def __hash__(self):
        return self.label.__hash__()

