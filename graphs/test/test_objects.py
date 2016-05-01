from itertools import permutations

import pytest

from ..objects import Graph, Node


class TestGraph:
    @pytest.fixture
    def foo_node(self):
        return Node(label='foo')

    @pytest.fixture
    def bar_node(self):
        return Node(label='bar')

    def test_equality(self):
        graph = Graph()
        assert graph == {}

        another_graph = Graph()
        assert graph == another_graph

    def test_add_node(self, foo_node):
        graph = Graph()
        graph.add(foo_node)
        assert graph == {foo_node.label: set()}

        graph = Graph()
        graph.add(foo_node.label)
        assert graph == {foo_node.label: set()}

        # Adding the same node, or a node with the same label, should raise.
        for node in [foo_node, foo_node.label]:
            with pytest.raises(ValueError):
                graph.add(node)

    def test_remove_node(self, foo_node, bar_node):
        graph = Graph()
        graph.add(foo_node)
        graph.remove(foo_node)
        assert graph == {}

        # If removing a connected node, we should remove all edges first.
        graph.add(foo_node)
        graph.add(bar_node)
        graph.connect(foo_node, bar_node)
        graph.remove(foo_node)
        assert graph == {bar_node.label: set()}

    def test_connect_nodes(self, foo_node, bar_node):
        graph = Graph()
        graph.add(foo_node)
        graph.add(bar_node)
        graph.connect(foo_node.label, bar_node.label)
        assert graph == {
            foo_node.label: {bar_node.label}, 
            bar_node.label: {foo_node.label}
        }

        # Connecting the same nodes again should have no effect.
        graph.connect(foo_node.label, bar_node.label)
        assert graph == {
            foo_node.label: {bar_node.label}, 
            bar_node.label: {foo_node.label}
        }

        # We should be able to connect by node also.
        graph.connect(foo_node, bar_node)
        assert graph == {
            foo_node.label: {bar_node.label}, 
            bar_node.label: {foo_node.label}
        }

    def test_disconnect_nodes(self, foo_node, bar_node):
        graph = Graph()
        graph.add(foo_node)
        graph.add(bar_node)
        graph.connect(foo_node.label, bar_node.label)
        graph.disconnect(foo_node.label, bar_node.label)
        assert graph == {foo_node.label: set(), bar_node.label: set()}

        # Disconnecting again should have no effect.
        graph.disconnect(foo_node.label, bar_node.label)
        assert graph == {foo_node.label: set(), bar_node.label: set()}

        # We should be able to disconnect by node also.
        graph.connect(foo_node.label, bar_node.label)
        graph.disconnect(foo_node, bar_node)
        assert graph == {foo_node.label: set(), bar_node.label: set()}

    def test_iterable(self, foo_node, bar_node):
        graph = Graph()
        graph.add(foo_node)
        for node in graph:
            assert node == foo_node.label

        i = iter(graph)
        assert next(i) == foo_node.label

    def test_getitem(self, foo_node, bar_node):
        graph = Graph()
        graph.add(foo_node)

        assert graph[foo_node] == []
        assert graph[foo_node.label] == []

        graph.add(bar_node)
        graph.connect(foo_node, bar_node)

        assert graph[foo_node] == [bar_node.label]
        assert graph[foo_node.label] == [bar_node.label]

        # The connected nodes should return in order. Since the order is not
        # fixed, the test can pass by chance. I'll test enough cases that this
        # is suffiently unlikely.
        graph = Graph()
        graph.add(foo_node)

        nodes = set('the quick brown fox jumps over the lazy dog')
        for node in nodes:
            graph.add(node)
            graph.connect(foo_node, node)

        assert graph[foo_node] == sorted(nodes)

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


class TestNode:
    def test_requires_label_to_instantiate(self):
        with pytest.raises(TypeError):
            node = Node()

        node = Node(label='foo')

    def test_label_is_immutable(self):
        node = Node(label='foo')
        assert node.label == 'foo'

        with pytest.raises(AttributeError):
            node.label = 'bar'

