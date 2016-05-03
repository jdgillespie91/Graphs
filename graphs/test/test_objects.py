from itertools import permutations

import pytest

from ..objects import Graph, Tree


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

    def test_iterable(self):
        graph = Graph()
        graph.add('foo')
        for node in graph:
            assert node == 'foo'

        i = iter(graph)
        assert next(i) == 'foo'

    def test_getitem(self):
        graph = Graph()
        graph.add('foo')

        assert graph['foo'] == []
        assert graph['foo'] == []

        graph.add('bar')
        graph.connect('foo', 'bar')

        assert graph['foo'] == ['bar']
        assert graph['foo'] == ['bar']

        # The connected nodes should return in order. Since the order is not
        # fixed, the test can pass by chance. I'll test enough cases that this
        # is suffiently unlikely.
        graph = Graph()
        graph.add('foo')

        nodes = set('the quick brown fox jumps over the lazy dog')
        for node in nodes:
            graph.add(node)
            graph.connect('foo', node)

        assert graph['foo'] == sorted(nodes)

    def test_sorted(self):
        # Permutations of the characters in this string will form the node
        # labels. The more unique characters there are, the less likely it is
        # that the test will pass by chance (note it could still happen, but
        # it's suffiently unlikely).
        for nodes in permutations('abcdef'):
            print(nodes)
            graph = Graph()
            for node in nodes:
                graph.add(node)

            i = iter(graph)
            for label in sorted(nodes):
                assert next(i) == label

    def test_bool(self):
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

