def get_label(node):
    try:
        return node.label
    except AttributeError:
        return node

