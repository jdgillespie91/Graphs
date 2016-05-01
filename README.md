Here's a quick investigation into depth-first and breadth-first search. The primary goal was to implement both algorithms recursively and non-recursively, an interesting exercise because of the relationship between recursion and the concept of a stack.

To aid this, I've built a very small Python library that can be used to build graphs. These graphs can then be searched using one of the four algorithms available in `graphs.search`.

### Usage

Instantiate an empty graph

```python
>>> graph = graphs.Graph() 
```
Add a node

```python
>>> node = graphs.Node(label='A')
>>> graph.add(node)
>>> graph
{'A': set()}
```

Add another node and connect it

```python
>>> graph.add('B')
>>> graph.connect('A', 'B')
{'A': {'B'}, 'B': {'A'}}
```

The graph is then traversable.

```python
>>> graphs.search.breadth_first_search(graph)
['A', 'B']
```

