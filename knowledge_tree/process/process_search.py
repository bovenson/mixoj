# coding: utf-8_knowledge_tree_nodes
import re
from knowledge_tree.search import search_manager
from knowledge_tree.db.db_operations import get_knowledge_tree


def process_search(_results, _knowledge_tree_nodes):
    """
    给出几个搜索引擎/博客/其他的搜索结果及关键字, 返回该内容与各个关键字的关系权重
    _results: 搜索结果
    _knowledge_tree: 知识树结点集
    """
    # 搜索结果是以搜索引擎名或者博客名等为关键字的字典, 需要遍历
    # 循环每个搜索结果
    # print(len(_results))
    for _result in _results.values():
        # print(_result)
        # 循环每个节点
        for _node in _knowledge_tree_nodes:
            # 循环每个节点的关键字
            # 在搜索结果中对关键字查找并计数, 以计数代表权重
            cnt = 0
            for _key_word in _node.key_words:
                # if _key_word == "DFS":
                #     print(len(re.findall(_key_word, _result, flags=re.IGNORECASE)))
                cnt += len(re.findall(_key_word, _result, flags=re.IGNORECASE))
                pass
            # 记录权重
            _node.weight += cnt
            pass
        pass
        # # 计数, 来判断最可能的分类
        # cnt = 0
        # for _key_word in _key_words:
        #     # 如果关键字是字符串
        #     if isinstance(_key_word, str):
        #         cnt += len(re.findall(_key_word, _result, flags=True))
        #     # 如果关键字是数组(几个关键字同义)
        #     elif isinstance(_key_word, tuple):
        #         for item in _key_word:
        #             cnt += len(re.findall(item, _result, flags=True))
        #     pass
        # 记录次数
    pass


if __name__ == "__main__":
    # 得到知识树
    knowledge_tree_nodes = get_knowledge_tree()
    for node in knowledge_tree_nodes:
        print(node.name, ": ", node.weight)
    pass
