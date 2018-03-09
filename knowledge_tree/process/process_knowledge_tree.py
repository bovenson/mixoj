# coding: utf-8


def add_parent_weight_to_children(_knowledge_tree_nodes):
    # 如果_knowledge_tree_nodes 类型不符合, 退出
    if not isinstance(_knowledge_tree_nodes, list):
        return None
    for _node in _knowledge_tree_nodes:
        # 如果当前节点没有被处理过, 则递归处理
        if not _node.processed:
            _recursion_process(_knowledge_tree_nodes, _node)
            pass
        pass
    pass


def _recursion_process(_knowledge_tree_nodes, _node):
    # print("处理节点:", _node.name, " weight:", _node.weight)
    if _node.pid < 0:
        return _node.weight
    if _node.processed:
        return _node.weight

    _parent_node_pos = _node.parent_pos
    _parent = _knowledge_tree_nodes[_parent_node_pos]
    _node.weight = _node.weight + _recursion_process(_knowledge_tree_nodes, _parent)
    # print(_node.name, ": ", _node.weight)
    return _node.weight
    pass


# def get_matches_sort_by_weight(_knowledge_tree):
#     """根据已经算好权重的树, 按照权重排序"""
# sorted(_knowledge_tree, key=_knowledge_tree_sort_key)
# return _knowledge_tree
# pass


def get_best_match(_knowledge_tree):
    if not isinstance(_knowledge_tree, list) or len(_knowledge_tree) < 1:
        return None
    _best_match_node = _knowledge_tree[0]
    for _node in _knowledge_tree:
        if _node.weight > _best_match_node.weight:
            _best_match_node = _node
        pass
    return _best_match_node
    pass


# def _knowledge_tree_sort_key(_node):
#     return _node.weight
#     pass


def clear_knowledge_tree(_knowledge_tree):
    for _node in _knowledge_tree:
        _node.weight = 0
        _node.processed = False
    pass
