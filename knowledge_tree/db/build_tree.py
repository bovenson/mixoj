# coding: utf-8
from knowledge_tree.db.db_operations import add_node, get_id_by_name_and_parent_name


def build_tree():
    add_node(_pid=-1, _name="数论", _synonym="数学,几何")
    add_node(_pid=-1, _name="模拟", _synonym="")
    add_node(_pid=-1, _name="动规", _synonym="动态规划,dp")

    # 图
    add_node(_pid=-1, _name="图", _synonym="")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="图", _parent_name=None), _name="最短路", _synonym="")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="图", _parent_name=None), _name="最长路", _synonym="")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="图", _parent_name=None), _name="最大流", _synonym="")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="图", _parent_name=None), _name="最小流", _synonym="")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="图", _parent_name=None),
             _name="松弛", _synonym="Relaxation")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="图", _parent_name=None),
             _name="Dijkstra", _synonym="迪杰斯特拉")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="图", _parent_name=None),
             _name="Floyd", _synonym="弗洛伊德")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="图", _parent_name=None),
             _name="DFS", _synonym="深度优先,深搜")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="图", _parent_name=None),
             _name="BFS", _synonym="广度优先,广搜")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="图", _parent_name=None),
             _name="拓扑排序", _synonym="")

    # 树
    add_node(_pid=-1, _name="树", _synonym="")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="树", _parent_name=None),
             _name="DFS", _synonym="深度优先,深搜")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="树", _parent_name=None), _name="BFS",
             _synonym="广度优先,广搜")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="树", _parent_name=None), _name="二叉树",
             _synonym="")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="二叉树", _parent_name="树"), _name="二叉搜索树",
             _synonym="")

    # 排序
    add_node(_pid=-1, _name="排序", _synonym="")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="排序", _parent_name=None), _name="快速排序",
             _synonym="快排 quicksort,qsort quick_sort")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="排序", _parent_name=None), _name="堆排序",
             _synonym="heapsort,heap_sort,最小堆,最大堆")
    # 分治
    add_node(_pid=-1, _name="分治", _synonym="")
    pass

    # 贪心
    add_node(_pid=-1, _name="贪心", _synonym="")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="贪心", _parent_name=None), _name="活动选择",
             _synonym="")
    add_node(_pid=get_id_by_name_and_parent_name(_node_name="贪心", _parent_name=None), _name="哈夫曼编码",
             _synonym="赫夫曼编码")


if __name__ == "__main__":
    build_tree()
    pass

