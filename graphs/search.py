def breadth_first_search(graph):
    discovered = []
    queue = []

    start_node = next(iter(graph))
    queue.append(start_node)

    while queue:
        node = queue.pop(0)
        if node not in discovered:
            discovered.append(node)
            for connected_node in graph[node]:
                queue.append(connected_node)

    return discovered


def recursive_breadth_first_search(graph, queue=None, discovered=None):
    if queue is None:
        queue = [next(iter(graph))]

    if discovered is None:
        discovered = []

    try:
        node = queue.pop(0)
    except IndexError:
        return discovered
    else:
        if node not in discovered:
            discovered.append(node)
            queue.extend(graph[node])
        return recursive_breadth_first_search(graph, queue=queue, discovered=discovered)


def depth_first_search(graph):
    discovered = []
    stack = []

    start_node = next(iter(graph))
    stack.append(start_node)

    while stack:
        node = stack.pop()
        if node not in discovered:
            discovered.append(node)
            for connected_node in reversed(graph[node]):
                stack.append(connected_node)

    return discovered


def recursive_depth_first_search(graph, node=None, discovered=None):
    if not node:
        node = next(iter(graph))

    if not discovered:
        discovered = []

    if node not in discovered:
        discovered.append(node)
        for connected_node in graph[node]:
            recursive_depth_first_search(graph, connected_node, discovered)

    return discovered

