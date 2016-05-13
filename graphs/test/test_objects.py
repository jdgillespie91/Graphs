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
        assert {} == tree

    def test_insert_into_empty_tree(self):
        tree = Tree()
        with pytest.raises(TypeError):
            tree.insert('A')

        node = Node('A')
        tree = Tree()
        tree.insert(node)
        assert {node: set()} == tree
        assert node == tree.root

    def test_instantiate_tree_with_node(self):
        node = Node('A')
        tree = Tree(node)
        assert {node: set()} == tree
        assert node == tree.root

    def test_insert(self):
        # Define some nodes.
        a_node = Node('A')
        b_node = Node('B')
        c_node = Node('C')
        d_node = Node('D')
        e_node = Node('E')
        f_node = Node('F')
        g_node = Node('G')
        h_node = Node('H')
        i_node = Node('I')
        j_node = Node('J')

        # Insert the nodes.
        tree = Tree(f_node)
        for node in [c_node, i_node, a_node, d_node, h_node, j_node, b_node, e_node, g_node]:
            tree.insert(node)

        # Verify the result.
        assert tree == {
            a_node: {b_node, c_node},
            b_node: {a_node},
            c_node: {a_node, d_node, f_node},
            d_node: {c_node, e_node},
            e_node: {d_node},
            f_node: {c_node, i_node},
            g_node: {h_node},
            h_node: {g_node, i_node},
            i_node: {f_node, h_node, j_node},
            j_node: {i_node}
        }


class TestNode:
    def test_label(self):
        node = Node('A')
        assert 'A' == node.label

    def test_nodes_can_be_sorted(self):
        foo = Node('foo')
        bar = Node('bar')
        assert [bar, foo] == sorted([foo, bar])

    def test_node_comparison(self):
        foo = Node('foo')
        assert not 'foo' == foo

        with pytest.raises(TypeError):
            'foo' > foo

    def test_behaviour_of_node_children(self):
        foo = Node('foo')

        # The children should be None initially.
        for ancestor in [foo.left_child, foo.right_child]:
            assert ancestor is None

        # The children may be set.
        foo.left_child = 'bar'
        foo.right_child = 'baz'
