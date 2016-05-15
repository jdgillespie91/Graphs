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

    def _connect(self, first_node, second_node):
        try:
            self._graph[first_node].add(second_node)
        except KeyError:
            raise KeyError('"{}" is not in the graph'.format(first_node))

    def connect(self, first_node, second_node):
        self._connect(first_node, second_node)
        self._connect(second_node, first_node)

    def _disconnect(self, first_node, second_node):
        try:
            self._graph[first_node].discard(second_node)
        except KeyError:
            raise KeyError('"{}" is not in the graph'.format(first_node))

    def disconnect(self, first_node, second_node):
        self._disconnect(first_node, second_node)
        self._disconnect(second_node, first_node)

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
        self._root = None
        if node:
            self.insert(node)

    def _add(self, node):
        self._graph.add(node)

    def _connect(self, first_node, second_node):
        self._graph.connect(first_node, second_node)

    def _insert(self, node, subroot):
        if node < subroot:
            if subroot.left_child:
                self._insert(node, subroot.left_child)
            else:
                subroot.left_child = node
                self._add(node)
                self._connect(node, subroot)
        elif node > subroot:
            if subroot.right_child:
                self._insert(node, subroot.right_child)
            else:
                subroot.right_child = node
                self._add(node)
                self._connect(node, subroot)

    def insert(self, node):
        if not isinstance(node, Node):
            raise TypeError('Trees must contain Nodes')

        if not self._graph:
            self._add(node)
            self._root = node
        else:
            self._insert(node, self._root)

    @property
    def root(self):
        return self._root

    def __eq__(self, other):
        return self._graph.__eq__(other)

    def __ne__(self, other):
        return self._graph.__ne__(other)

    def __repr__(self):
        return self._graph.__repr__()

    def __iter__(self):
        return self._graph.__iter__()

    def __next__(self):
        return self._graph.__next__()

    def __getitem__(self, node):
        return self._graph.__getitem__(node)


@total_ordering
class Node:
    def __init__(self, label):
        self._label = label
        self._left_child = None
        self._right_child = None

    @property
    def label(self):
        return self._label

    @property
    def left_child(self):
        return self._left_child

    @left_child.setter
    def left_child(self, value):
        self._left_child = value

    @property
    def right_child(self):
        return self._right_child

    @right_child.setter
    def right_child(self, value):
        self._right_child = value

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.label.__eq__(other.label)

    def __lt__(self, other):
        if not isinstance(other, Node):
            raise TypeError('Only Node types can be compared')
        return self.label.__lt__(other.label)

    def __hash__(self):
        return self.label.__hash__()

    def __repr__(self):
        return self.label.__repr__()
