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
        if not self._graph:
            self._add(node)
            self._root = node
        else:
            self._insert(node, self._root)

    def _insert(self, node, subroot):
        # TODO Now that it's working, tidy this method.

        # If no leaves, add it.
        if not self._graph[subroot]:
            self._add(node)
            self._connect(subroot, node)
            return

        # If one leaf... it's hard!
        # A node can have one leaf if it is a root node or the last node on a
        # branch. Anything else will have more than one leaf (potentially both
        # upstream and downstream, but since we don't consider hierarchy
        # currently, that's irrelevant). I think this is a fact to exploit, and
        # is in fact the specific case below relies on this.
        if len(self._graph[subroot]) == 1:
            root = subroot
            leaf = self._graph[subroot][0]

            # If not handled specifically, we get infinite recursion.
            if (root < node < leaf or root > node > leaf) and root == self._root:
                self._add(node)
                self._connect(node, leaf)
                return
            elif root < node < leaf or root > node > leaf:
                self._add(node)
                self._connect(node, root)
                return

            if root < leaf:
                if node < root:
                    self._add(node)
                    self._connect(node, root)
                    return
                else:
                    self._insert(node, subroot=leaf)
            else:
                if node > root:
                    self._add(node)
                    self._connect(node, root)
                    return
                else:
                    self._insert(node, subroot=leaf)

        # If two leaves, insert it against the appropriate leaf.
        if len(self._graph[subroot]) == 2:
            if node < subroot:
                self._insert(node, subroot=self._graph[subroot][0])
            else:
                self._insert(node, subroot=self._graph[subroot][1])

    def __eq__(self, other):
        return self._graph.__eq__(other)

    def __ne__(self, other):
        return self._graph.__ne__(other)

    def __repr__(self):
        return self._graph.__repr__()
