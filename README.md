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

