# coding: utf-8
import re

from knowledge_tree.db.common_db import CommonDB
from knowledge_tree.db.models import KnowledgeTreeNode
from knowledge_tree.db.db_init import DB_TABLE_NAME
from knowledge_tree.public.string_operations import str_is_equal_ignore_case, get_keywords


def add_node(_pid, _name, _synonym=""):
    """为知识树增加节点"""
    # 初始化数据库
    _db = CommonDB()
    sql = "INSERT INTO " + DB_TABLE_NAME + "(pid, name, synonym) VALUES(%s, %s ,%s)"
    params = (_pid, _name, _synonym)
    try:
        if get_id_by_pid_and_name(_pid, _name) is not None:
            raise Exception("节点已存在")
            pass
        _db.execute(sql, params=params)
        _db.commit()
    except Exception as e:
        print("新建节点时出错: ", e)
    else:
        pass
        # print("成功建立节点: ", _name)
    finally:
        if _db is not None:
            _db.close()
    pass


def get_id_by_pid_and_name(_pid, _node_name):
    """给出节点名, 及父节点id, 返回节点id"""
    _db = CommonDB()
    if _node_name is None or str(_node_name).strip() == "":
        return None
    sql = "SELECT id FROM " + DB_TABLE_NAME + " WHERE name=%s and pid=%s"
    _db.execute(sql, (_node_name, _pid))
    _result = _db.fetchone()
    if isinstance(_result, tuple):
        # print(_result[0])
        return _result[0]
        pass
    return None
    pass


def get_id_by_name(_node_name):
    """给出节点名, 返回节点id"""
    _db = CommonDB()
    if _node_name is None or str(_node_name).strip() == "":
        return None
    sql = "SELECT id FROM " + DB_TABLE_NAME + " WHERE name=%s"
    _db.execute(sql, (_node_name,))
    _result = _db.fetchone()
    if isinstance(_result, tuple):
        # print(_result[0])
        return _result[0]
        pass
    return None
    pass


def get_id_by_name_and_parent_name(_node_name, _parent_name):
    """给出节点名, 返回节点id"""
    _db = CommonDB()
    if _node_name is None or str(_node_name).strip() == "":
        return None
    sql = "SELECT id,pid FROM " + DB_TABLE_NAME + " WHERE name=%s"
    _db.execute(sql, (_node_name,))
    _results = _db.fetchall()
    for _result in _results:
        if isinstance(_result, tuple):
            _pid = _result[1]
            _maybe_parent_name = get_name_by_id(_pid)
            # 如果得到的父节点和给出的父节点名称相同, 则返回
            if str_is_equal_ignore_case(_maybe_parent_name, _parent_name):
                return _result[0]
            pass
    return None
    pass


def get_name_by_id(_id):
    """给出节点id返回节点名称"""
    _db = CommonDB()
    if _id is None or _id < 0:
        return None
    sql = "SELECT name FROM " + DB_TABLE_NAME + " WHERE id=%s"
    _db.execute(sql, (_id,))
    _result = _db.fetchone()
    if isinstance(_result, tuple):
        return _result[0]
        pass
    return None
    pass


def get_knowledge_tree_nodes():
    """从数据库查询知识树结构, 返回节点集"""
    _arr = []
    _db = CommonDB()
    sql = "SELECT id,pid,name,synonym FROM " + DB_TABLE_NAME
    try:
        _db.execute(sql)
        for item in _db.fetchall():
            _node = KnowledgeTreeNode(cid=item[0], pid=item[1], name=item[2], synonym=item[3])
            _arr.append(_node)
        pass
    except Exception as e:
        print("查询知识树结构时出错: ", e)
    return _arr
    pass


def build_tree(_nodes):
    """根据节点建树"""
    # 构建节点id 和 节点在list位置 的字典映射
    id_pos = {}
    for _i in range(0, len(_nodes)):
        id_pos[_nodes[_i].id] = _i
    # print(id_pos)
    # 修改节点集中每个节点的parent_pos
    for _node in _nodes:
        # 设置父节点位置
        if _node.pid < 0:
            _node.parent_pos = -1
        else:
            _node.parent_pos = id_pos[_node.pid]

        # 解析每个节点的关键字
        # 添加节点名字到关键字
        _key_words = [_node.name]
        # 将节点同义词添加到关键字集
        for _key_word in get_keywords(_node.synonym):
            # 如果是空关键字, 跳过
            if _key_word.strip() == "":
                continue
            if not isinstance(_key_word, str):
                _key_word = str(_key_word)
            _key_words.append(_key_word)
        _node.key_words = _key_words
    return _nodes
    pass


def get_knowledge_tree():
    """根据查询的知识树结构, 构建知识树, 也就是将 KnowledgeTreeNode 的parent_pos给填上, 父节点位置是父节点在 list 中的位置"""
    return build_tree(get_knowledge_tree_nodes())
    pass

NODE_DROPDOWN_MENU = """<a id='menu%s' onclick='javascript:(nodeMenu(this, %s, %s))'>
                        <span class="glyphicon glyphicon-menu-hamburger"
                        aria-hidden="true"></span></a>"""


def get_knowledge_tree_json(_pid=-1):
    """得到可以转换成json格式的树结构"""
    _nodes = []
    _db = CommonDB()
    sql = "SELECT id,pid,name,synonym FROM " + DB_TABLE_NAME + " WHERE pid=%s"
    params = (_pid,)
    try:
        _db.execute(sql=sql, params=params)
        _reses = _db.fetchall()
        _db.close()
        for _res in _reses:
            _node = {"id": _res[0],
                     "pid": _res[1],
                     "text": _res[2],
                     "synonym": _res[3],
                     "href": "javascript:nodeNameClick(%s)" % _res[0],
                     # "tags": ["<a href='javascript:(nodeMenu(" + str(_res[0]) + ", " + str(_res[1]) + "))'>哈哈</a>"],
                     "tags": [NODE_DROPDOWN_MENU % (_res[0], _res[0], _res[1])],
                     }
            _child_nodes = get_knowledge_tree_json(_res[0])
            if len(_child_nodes) > 0:
                _node["nodes"] = _child_nodes
            _nodes.append(_node)
        # print(_reses)
        pass
    except Exception as e:
        print("获取知识树时出错：", e)
        pass
    return _nodes
    pass


def get_node_detail_by_id(_node_id):
    _data = {}
    _db = CommonDB()
    sql = "SELECT id,pid,name,synonym FROM " + DB_TABLE_NAME + " WHERE id=%s"
    params = (_node_id,)
    try:
        _db.execute(sql, params)
        _res = _db.fetchone()
        _db.close()
        if _res is not None:
            _data["id"] = _res[0]
            _data["pid"] = _res[1]
            _data["name"] = _res[2]
            _data["synonym"] = _res[3]
        pass
    except:
        pass
    return _data
    pass


def update_node(_node_id, _node_name, _node_synonym):
    _data = {}
    _db = CommonDB()
    sql = "UPDATE " + DB_TABLE_NAME + " SET name=%s,synonym=%s WHERE id=%s"
    params = (_node_name, _node_synonym, _node_id,)
    try:
        _db.execute(sql, params)
        _db.commit()
        _db.close()
        _data["res"] = "success"
        _data["msg"] = "更新成功"
    except Exception as e:
        # import traceback
        # traceback.print_exc()
        _data["res"] = "error"
        _data["msg"] = str(e)
        pass
    return _data
    pass


def add_child_node(_pid, _node_name, _node_synonym):
    _data = {}
    _db = CommonDB()
    sql = "INSERT INTO " + DB_TABLE_NAME + "(pid,name,synonym) VALUES(%s,%s,%s)"
    params = (_pid, _node_name, _node_synonym,)
    try:
        _db.execute(sql, params)
        _db.commit()
        _db.close()
        _data["res"] = "success"
        _data["msg"] = "添加子节点成功"
    except Exception as e:
        # import traceback
        # traceback.print_exc()
        _data["res"] = "error"
        _data["msg"] = str(e)
        pass
    return _data
    pass


def get_parent_id_by_id(_node_id):
    _data = None
    _db = CommonDB()
    sql = "SELECT pid FROM " + DB_TABLE_NAME + " WHERE id=%s"
    params = (_node_id,)
    try:
        _db.execute(sql, params)
        _res = _db.fetchall()
        _db.close()
        _data = _res[0][0]
    except Exception as e:
        import traceback
        traceback.print_exc()
        pass
    return _data
    pass


def delete_knowledge_tree_node(_node_id):
    _data = {}
    try:
        _db = CommonDB()
        # 找子节点并删除
        sql = "SELECT id FROM " + DB_TABLE_NAME + " WHERE pid=%s"
        params = (_node_id,)
        _db.execute(sql, params)
        _reses = _db.fetchall()
        _db.close()
        for _res in _reses:
            _cid = _res[0]
            delete_knowledge_tree_node(_cid)
            # print("cid:", _cid)
            pass

        # 删除该节点
        _db = CommonDB()
        sql = "DELETE FROM " + DB_TABLE_NAME + " WHERE id=%s"
        params = (_node_id,)
        _db.execute(sql, params)
        _db.commit()
        _db.close()

        _data["res"] = "success"
        _data["msg"] = "删除节点成功"
    except Exception as e:
        _data["res"] = "error"
        _data["msg"] = "删除节点时出错：" + str(e)
        import traceback
        traceback.print_exc()
        pass
    return _data
    pass


def get_all_knowledge_node_name():
    _data = []
    _db = CommonDB()
    sql = "SELECT name FROM " + DB_TABLE_NAME
    try:
        _db.execute(sql)
        _reses = _db.fetchall()
        _db.close()
        for _res in _reses:
            _data.append(_res[0])
        pass
    except:
        pass
    return _data
    pass

if __name__ == "__main__":
    # add_node(_pid=-1, _name="二分")
    # print(get_id_by_name("图"))
    # print(get_id_by_name_and_parent_name(_node_name="BFS", _parent_name="树"))
    # get_knowledge_tree()
    # for node in get_knowledge_tree():
    #     print(node.name, ": ", node.parent_pos)

    # print(get_knowledge_tree_json(-1))
    # print(get_node_detail_by_id(1))
    # print(get_parent_id_by_id(27))
    print(delete_knowledge_tree_node(1))
    pass
