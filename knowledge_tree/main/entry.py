# coding: utf-8
from knowledge_tree.db.db_operations import get_knowledge_tree, get_name_by_id
from knowledge_tree.process.process_knowledge_tree import add_parent_weight_to_children, get_best_match
from knowledge_tree.process.process_knowledge_tree import clear_knowledge_tree
from knowledge_tree.process.process_search import process_search
from knowledge_tree.search.search_manager import get_search_content

from mixojapp.models import Problem


def start_search(_search_content):
    """入口
    _search_content: 搜索内容
    """
    # 每次都建树, 慢点
    _knowledge_tree = get_knowledge_tree()
    # 得到搜索结果
    _search_res = get_search_content(_search_content)
    # print(_search_res)
    # 处理搜索结果
    process_search(_search_res, _knowledge_tree)
    # 对处理后的结果树再处理
    add_parent_weight_to_children(_knowledge_tree)
    # 按照权重得到结果
    _best_match = get_best_match(_knowledge_tree)

    # 如果搜索结果太少, 不分类
    if _best_match.weight < 3:
        return None

    return _best_match
    pass


def start_search_faster(_search_content, _knowledge_tree):
    """入口
    _search_content: 搜索内容
    _knowledge_tree: 建好的知识树, 每次用时要清除一些冗余数据
    """
    # 得到搜索结果
    _search_res = get_search_content(_search_content)
    # print(_search_res)
    # 处理搜索结果
    process_search(_search_res, _knowledge_tree)
    # 对处理后的结果树再处理
    add_parent_weight_to_children(_knowledge_tree)
    # 按照权重得到结果
    _best_match = get_best_match(_knowledge_tree)

    # 如果搜索结果太少, 不分类
    if _best_match.weight < 3:
        return None
    return _best_match
    pass


def get_result(_search_content):
    _res = {}
    _best_match = start_search(_search_content)
    if _best_match is not None:
        _res["pid"] = _best_match.pid
        _res["name"] = _best_match.name
        _res["id"] = _best_match.id
        _res["weight"] = _best_match.weight
    else:
        _res["pid"] = -1
        _res["name"] = "未分类"
        _res["id"] = -1
        _res["weight"] = -1
        pass
    return _res
    pass


def update_problem_knowledge_tree(_ojname, _problem_id):
    _res = {}
    _search_content = str(_ojname) + " " + str(_problem_id)
    try:
        _problem = Problem.objects.get(ojname=_ojname, sourceid=_problem_id)

        # 如果是uva 和 uvalive
        if _ojname.lower() == "uva" or _ojname.lower() == "uvalive":
            _problem_title = _problem.title
            _t_problem_id = _problem_title.split("-")[0]
            # print(_t_problem_id)
            _best_match = get_result(str(_ojname) + " " + str(_t_problem_id))
        else:
            _best_match = get_result(_search_content)
        if _best_match.get("id") is None or _best_match.get("id") < 0:
            _res["res"] = "error"
            _res["msg"] = "没有找到题目 " + _search_content + " 的分类"
            raise Exception()
        _problem.knowledge_tree_node_id = _best_match.get("id")
        _problem.knowledge_tree_node_name = _best_match.get("name")
        _problem.save()
        _res["res"] = "success"
        _res["msg"] = "成功更新题目 " + _search_content + " 分类:" + _best_match.get("name")
        pass
    except Problem.DoesNotExist:
        _res["res"] = "error"
        _res["msg"] = "没有找到题目 " + _search_content
        pass
    except Exception as e:
        if _res.get("res") is None:
            _res["res"] = "error"
            _res["msg"] = "更新题目 " + _search_content + " 知识树时出错:" + str(e)
        pass
    return _res
    pass

if __name__ == "__main__":
    # 得到知识树, 为了减少对数据的访问及提高效率,
    knowledge_tree = get_knowledge_tree()
    for pid in range(2160, 2199):
        search_content = "poj " + str(pid)
        try:
            best_match = start_search_faster(search_content, knowledge_tree)
            print("对", search_content, "分类结果:")
            print("best match-> parent name:", get_name_by_id(best_match.pid) , " name:", best_match.name)
        except Exception as e:
            print("对 " + search_content + " 构建知识树时出错:", e)
        # 清除知识树冗余数据
        clear_knowledge_tree(knowledge_tree)
    pass
