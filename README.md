[![Build Status](https://travis-ci.org/jdgillespie91/Graphs.svg?branch=master)](https://travis-ci.org/jdgillespie91/Graphs)

Here's a quick investigation into depth-first and breadth-first search. The primary goal was to implement both algorithms recursively and non-recursively, an interesting exercise because of the relationship between recursion and the concept of a stack.

To aid this, I've built a very small Python library that can be used to build graphs. These graphs can then be searched using one of the four algorithms available in `graphs.search`.

### Usage

#### Graphs

Instantiate an empty graph

```python
>>> graph = graphs.Graph() 
```

Add a node

```python
>>> graph.add('A')
>>> graph
{'A': set()}
```

Add another node and connect it

```python
>>> graph.add('B')
>>> graph.connect('A', 'B')
>>> graph
{'A': {'B'}, 'B': {'A'}}
```

The graph is then traversable.

```python
>>> graphs.search.breadth_first_search(graph)
['A', 'B']
```

#### Trees

Instantiate an empty tree

```python
>>> tree = graphs.Tree()
```

Insert a node (note that the type is now important)

```python
>>> node = graphs.Node('B')
>>> tree.insert(node)
>>> tree
{'B': set()}
```

The tree is then traversable.

```python
>>> node = graphs.Node('A')
>>> tree.insert(node)
>>> graphs.search.breadth_first_search(tree)
['B', 'A']
```
