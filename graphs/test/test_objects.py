from itertools import permutations

import pytest

from ..objects import Graph, Node, Tree


class TestGraph:
    def test_equality(self):
        graph = Graph()
        assert graph == {}

        another_graph = Graph()
        assert graph == another_graph

    def test_add_node(self):
        graph = Graph()
        graph.add('foo')
        assert graph == {'foo': set()}

        # Adding the same node should raise.
        with pytest.raises(ValueError):
            graph.add('foo')

    def test_remove_node(self):
        graph = Graph()
        graph.add('foo')
        graph.remove('foo')
        assert graph == {}

        # If removing a connected node, we should remove all edges first.
        graph.add('foo')
        graph.add('bar')
        graph.connect('foo', 'bar')
        graph.remove('foo')
        assert graph == {'bar': set()}

    def test_connect_nodes(self):
        graph = Graph()
        graph.add('foo')
        graph.add('bar')
        graph.connect('foo', 'bar')
        assert graph == {
            'foo': {'bar'},
            'bar': {'foo'}
        }

        # Connecting the same nodes again should have no effect.
        graph.connect('foo', 'bar')
        assert graph == {
            'foo': {'bar'},
            'bar': {'foo'}
        }

        # We should be able to connect by node also.
        graph.connect('foo', 'bar')
        assert graph == {
            'foo': {'bar'},
            'bar': {'foo'}
        }

    def test_disconnect_nodes(self):
        graph = Graph()
        graph.add('foo')
        graph.add('bar')
        graph.connect('foo', 'bar')
        graph.disconnect('foo', 'bar')
        assert graph == {'foo': set(), 'bar': set()}

        # Disconnecting again should have no effect.
        graph.disconnect('foo', 'bar')
        assert graph == {'foo': set(), 'bar': set()}

        # We should be able to disconnect by node also.
        graph.connect('foo', 'bar')
        graph.disconnect('foo', 'bar')
        assert graph == {'foo': set(), 'bar': set()}

    def test_iterating_over_graph(self):
        """ Ensure that we iterate over the nodes in order.

        When iterating over the graph, we should be iterating over the nodes
        in alphabetical order. Unfortunately, the order in which we add nodes
        has no impact on the order in which we iterate over them.

        It's possible that, by chance, we iterate over the graph
        alphabetically. As such, we test many graphs here to reduce the
        likelihood that a pass is by chance alone.

        """
        for nodes in permutations('abcdef'):
            graph = Graph()
            for node in nodes:
                graph.add(node)

            i = iter(graph)
            for label in sorted(nodes):
                assert next(i) == label

    def test_graph_lookup(self):
        graph = Graph()
        graph.add('foo')

        nodes = set('the quick brown fox jumps over the lazy dog')
        for node in nodes:
            graph.add(node)
            graph.connect('foo', node)

        assert graph['foo'] == sorted(nodes)

    def test_is_graph_empty(self):
        # An empty graph should return false.
        graph = Graph()
        assert not graph

        # A populated graph should return true.
        graph.add('A')
        assert graph


class TestTree:
    def test_empty_tree(self):
        tree = Tree()
        assert tree == {}

    def test_insert_into_empty_tree(self):
        tree = Tree()
        tree.insert('A')
        assert tree == {'A': set()}

    def test_instantiate_tree_with_node(self):
        tree = Tree('A')
        assert tree == {'A': set()}

    def test_insert(self):
        # TODO Split out tree types into separate tests then use parameterize.
        # Empty tree.
        tree = Tree()
        tree.insert('A')
        assert tree == {'A': set()}

        # Trees with no leaves.
        tree = Tree('B')
        tree.insert('A')
        assert tree == {'A': {'B'}, 'B': {'A'}}

        tree = Tree('B')
        tree.insert('C')
        assert tree == {'B': {'C'}, 'C': {'B'}}

        # Trees with one leaf where the root is bigger than the leaf.
        tree = Tree('D')
        tree.insert('B')
        tree.insert('A')
        assert tree == {'A': {'B'}, 'B': {'A', 'D'}, 'D': {'B'}}

        tree = Tree('D')
        tree.insert('B')
        tree.insert('C')
        assert tree == {'B': {'C', 'D'}, 'C': {'B'}, 'D': {'B'}}

        tree = Tree('D')
        tree.insert('B')
        tree.insert('E')
        assert tree == {'B': {'D'}, 'D': {'B', 'E'}, 'E': {'D'}}

        # Trees with one leaf where the root is bigger than the leaf.
        tree = Tree('B')
        tree.insert('D')
        tree.insert('A')
        assert tree == {'A': {'B'}, 'B': {'A', 'D'}, 'D': {'B'}}

        tree = Tree('B')
        tree.insert('D')
        tree.insert('C')
        assert tree == {'B': {'D'}, 'C': {'D'}, 'D': {'B', 'C'}}

        tree = Tree('B')
        tree.insert('D')
        tree.insert('E')
        assert tree == {'B': {'D'}, 'D': {'B', 'E'}, 'E': {'D'}}

        # Trees with two leaves.
        tree = Tree('D')
        tree.insert('B')
        tree.insert('F')
        tree.insert('A')
        assert tree == {'A': {'B'}, 'B': {'A', 'D'}, 'D': {'B', 'F'}, 'F': {'D'}}

        tree = Tree('D')
        tree.insert('B')
        tree.insert('F')
        tree.insert('C')
        assert tree == {'B': {'C', 'D'}, 'C': {'B'}, 'D': {'B', 'F'}, 'F': {'D'}}

        tree = Tree('D')
        tree.insert('B')
        tree.insert('F')
        tree.insert('E')
        assert tree == {'B': {'D'}, 'D': {'B', 'F'}, 'E': {'F'}, 'F': {'D', 'E'}}

        tree = Tree('D')
        tree.insert('B')
        tree.insert('F')
        tree.insert('G')
        assert tree == {'B': {'D'}, 'D': {'B', 'F'}, 'F': {'D', 'G'}, 'G': {'F'}}

        # TODO Write a failing test (or test case within this test) to cover bigger trees. At this
        # point, it's probably necessary to automate this, but we'll see.
        tree = Tree('F')
        for node in ['C', 'I', 'A', 'D', 'H', 'J', 'B', 'E', 'G']:
            tree.insert(node)
        assert tree == {
            'A': {'B', 'C'},
            'B': {'A'},
            'C': {'A', 'D', 'F'},
            'D': {'C', 'E'},
            'E': {'D'},
            'F': {'C', 'I'},
            'G': {'H'},
            'H': {'G', 'I'},
            'I': {'F', 'H', 'J'},
            'J': {'I'}
        }


class TestNode:
    def test_label(self):
        node = Node('A')
        assert 'A' == node.label

    def test_nodes_can_be_sorted(self):
        foo = Node('foo')
        bar = Node('bar')
        assert [bar, foo] == sorted([foo, bar])

    def test_nodes_cannot_be_compared_to_other_types(self):
        foo = Node('foo')
        with pytest.raises(TypeError):
            'foo' == foo


class TestGraphOfNodes:
    def test_behaviour(self):
        """ Verify some standard behaviour of a graph.

        First, nodes must be hashable so that the dictionary lookup in the
        graph works correctly. Second, nodes must be comparable so that they
        may be returned in order and iterated over in order.

        """
        graph = Graph()
        foo = Node('foo')
        bar = Node('bar')
        baz = Node('baz')

        # Ensure the dictionary lookup works.
        graph.add(foo)
        graph.add(bar)
        graph.add(baz)
        graph.connect(foo, bar)
        graph.connect(foo, baz)
        graph.connect(bar, baz)

        # Ensure the nodes are returned in order.
        assert [bar, baz] == graph[foo]
        assert [baz, foo] == graph[bar]
        assert [bar, foo] == graph[baz]

        # Ensure the nodes are iterated over in order.
        i = iter(graph)
        for label in sorted([foo, bar, baz]):
            assert next(i) == label
