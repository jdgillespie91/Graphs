import pytest

from ..objects import Graph, Node, Tree
from ..search import (
    breadth_first_search, recursive_breadth_first_search,
    depth_first_search, recursive_depth_first_search
)


class TestSearchGraph:
    @pytest.fixture
    def graph(self):
        graph = Graph()

        for node in 'ABCDEFG':
            graph.add(node)

        for pair in ['AB', 'AC', 'AF', 'AG', 'BC', 'BD', 'CE', 'FG']:
            graph.connect(pair[0], pair[1])

        return graph

    def test_breadth_first_search(self, graph):
        expected_route = list('ABCFGDE')
        actual_route = breadth_first_search(graph)
        assert expected_route == actual_route

    def test_recursive_breadth_first_search(self, graph):
        expected_route = list('ABCFGDE')
        actual_route = recursive_breadth_first_search(graph)
        assert expected_route == actual_route

    def test_depth_first_search(self, graph):
        expected_route = list('ABCEDFG')
        actual_route = depth_first_search(graph)
        assert expected_route == actual_route

    def test_recursive_depth_first_search(self, graph):
        expected_route = list('ABCEDFG')
        actual_route = recursive_depth_first_search(graph)
        assert expected_route == actual_route


class TestSearchTree:
    @pytest.fixture
    def tree(self):
        tree = Tree()

        for node in [Node(x) for x in list('EBGACFH')]:
            tree.insert(node)

        return tree

    def test_breadth_first_search(self, tree):
        expected_route = [Node(x) for x in list('EBGACFH')]
        actual_route = breadth_first_search(tree)
        assert expected_route == actual_route

    def test_recursive_breadth_first_search(self, tree):
        expected_route = [Node(x) for x in list('EBGACFH')]
        actual_route = recursive_breadth_first_search(tree)
        assert expected_route == actual_route

    def test_depth_first_search(self, tree):
        expected_route = [Node(x) for x in list('EBACGFH')]
        actual_route = depth_first_search(tree)
        assert expected_route == actual_route

    def test_recursive_depth_first_search(self, tree):
        expected_route = [Node(x) for x in list('EBACGFH')]
        actual_route = recursive_depth_first_search(tree)
        assert expected_route == actual_route
