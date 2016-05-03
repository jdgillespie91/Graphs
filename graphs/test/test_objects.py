from itertools import permutations

import pytest

from ..objects import Graph


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

