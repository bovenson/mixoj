from knowledge_tree.db.common_db import CommonDB
from spider.stageone.db.db_operations import get_sources
import source_tree.build_source_tree
import time


def fixAnthor(oldAnthor, newAnthor, tableName):
    if oldAnthor is None or oldAnthor == '':
        return False
    if newAnthor is None or newAnthor == '':
        return False
    if tableName is None or tableName == '':
        return False
    if oldAnthor == 'Root':
        return True
    try:
        db_hundler = CommonDB()
        db_hundler.execute("UPDATE " + tableName + " SET parent = %s \
        WHERE parent = %s", (newAnthor, oldAnthor))
        db_hundler.commit()
    except Exception as e:
        print(e)
        db_hundler.close()
        return False

    db_hundler.close()
    return True


def deleteNodeByName(name):
    data = {}
    if name is None or name == '':
        return False
    parent = findParentByName(name)
    type = findTypeByName(name)
    if parent is None or type is None:
        return False
    try:
        db_hundler = CommonDB()
        db_hundler.execute("DELETE FROM sourcetree WHERE name = %s", (name))
        db_hundler.execute("DELETE FROM " + type + " WHERE name = %s", (name))
        db_hundler.commit()
        fixAnthor(name, parent, type)
        fixAnthor(name, parent, 'sourcetreeref')
        fixAnthor(name, parent, 'sourcetree')
        data["res"] = "success"
        data["msg"] = "删除节点成功"
    except Exception as e:
        data["res"] = "error"
        data["msg"] = str(e)
    db_hundler.close()
    return data


def addNode(name, parent):
    data = {}
    if name is None or name == '':
        return False
    if parent is None or parent == '':
        return False

    if findNodeByName(name) == True:
        data["res"] = "error"
        data["msg"] = "Already Exists!"
        return data
    try:
        db_hundler = CommonDB()
        db_hundler.execute("INSERT INTO sourcetree(name, parent, needShow, haveProblem, theType) \
                        VALUES(%s, %s, %s, %s, %s)", (name, parent, 1, 0, "custom"))
        db_hundler.execute("INSERT INTO custom(name, parent, abbr) \
            VALUES(%s, %s, %s)", (name, parent, ""))
        db_hundler.commit()
        data["res"] = "success"
        data["msg"] = "添加子节点成功"
        source_tree.build_source_tree.updateProblem('%', '%', False)
    except Exception as e:
        data["res"] = "error"
        data["msg"] = str(e)
    db_hundler.close()
    return data


def fixProblemCount(name, num):
    if name is None or name == "":
        return False
    try:
        db_hundler = CommonDB()
        db_hundler.execute("SELECT parent, haveProblem FROM sourcetree WHERE name = %s", (name))
        res = db_hundler.fetchone()
        db_hundler.close()
        if isinstance(res, tuple):
            cnt = max(0, int(res[1]) + num)
            db_hundler = CommonDB()
            db_hundler.execute("UPDATE sourcetree SET haveProblem = %s WHERE name = %s", (cnt, name))
            db_hundler.commit()
            db_hundler.close()
            if name == 'Root':
                return True
            return fixProblemCount(res[0], num)
    except Exception as e:
        print(e)
    return False

def addProblem(id, ojname, newParent):
    data = {}
    res = get_sources(id, ojname)
    source = ""
    if len(res) > 0:
        source = source_tree.build_source_tree.simpleSource(res[0][0])
    print(source)
    try:
        db_hundler = CommonDB()
        db_hundler.execute("SELECT parent FROM sourcetreeref WHERE source = %s", \
                           (source))
        res = db_hundler.fetchall()
        length = len(res)
        if length > 0:
            oldParent = res[0][0]
        if oldParent == newParent:
            data["res"] = "error"
            data["msg"] = "无效位置"
            return data
        db_hundler.execute("UPDATE sourcetreeref SET parent = %s, isUser = %s WHERE source = %s", \
                           (newParent, 1, source))
        db_hundler.commit()
        db_hundler.close()
        fixProblemCount(oldParent, -length)
        fixProblemCount(newParent, +length)
        data["res"] = "success"
        data["msg"] = "更新题目成功"
    except Exception as e:
        data["res"] = "error"
        data["msg"] = str(e)
    return data


def findTypeByName(name):
    if name is None or name == '':
        return False
    try:
        db_hundler = CommonDB()
        db_hundler.execute("SELECT theType FROM sourcetree WHERE name = %s", (name))
        res = db_hundler.fetchone()
        if isinstance(res, tuple):
            return res[0]
    except Exception as e:
        print(e)
    db_hundler.close()
    return None


def findParentByName(name):
    if name is None or name == '':
        return None
    try:
        db_hundler = CommonDB()
        db_hundler.execute("SELECT parent FROM sourcetree WHERE name = %s", (name))
        res = db_hundler.fetchone()
        if isinstance(res, tuple):
            return res[0]
    except Exception as e:
        print(e)
    db_hundler.close()
    return None


def findNodeByName(name):
    if name is None or name == '':
        return False
    try:
        db_hundler = CommonDB()
        db_hundler.execute("SELECT * FROM sourcetree WHERE name = %s", (name))
        res = db_hundler.fetchone()
        if isinstance(res, tuple):
            return True
    except Exception as e:
        print(e)
    db_hundler.close()
    return False


NODE_DROPDOWN_MENU = """<a id='menu%s' onclick="javascript:nodeMenu(this, '%s', '%s')">
    <span class="glyphicon glyphicon-menu-hamburger"
    aria-hidden="true"></span></a>"""


def get_source_tree_json(level, date, pid="Root"):
    nodes = []
    _db = CommonDB()
    sql = "SELECT * FROM sourcetree WHERE parent = %s"
    params = (pid,)
    try:
        _db.execute(sql=sql, params=params)
        res = _db.fetchall()
        for entry in res:
            title = entry[0]
            parent = entry[1]
            if entry[2] == 0 or entry[3] == 0:
                continue
            node = {
                "text": title,
                "parent": parent,
                "tags": [NODE_DROPDOWN_MENU % (str(title).replace(" ", ""), title, parent)],
            }
            childNode = get_source_tree_json(level, date, title)
            findRef(childNode, title, level, date)
            if len(childNode) > 0:
                node['nodes'] = childNode
            nodes.append(node)
        if pid == 'Root':
            findRef(nodes, 'Root', level, date)
        pass
    except Exception as e:
        print(e)
        pass
    return nodes


def findRef(nodes, parent, level, date):
    _db = CommonDB()
    sql = "SELECT * FROM sourcetreeref WHERE parent = %s AND level LIKE %s"
    params = (parent, level)
    try:
        curYear = int(time.localtime()[0])
        _db.execute(sql=sql, params=params)
        res = _db.fetchall()
        for entry in res:
            isOK = False
            title = entry[0]
            _date = 0
            if entry[2] != 'none':
                _date = int(entry[2])
            if date == 'Last 1 Year':
                if abs(curYear - _date) <= 1:
                    isOK = True
            elif date == 'Last 5 Years':
                if abs(curYear - _date) <= 5:
                    isOK = True
            elif date == 'Last 10 Years':
                if abs(curYear - _date) <= 10:
                    isOK = True
            else:
                isOK = True
            if isOK == True:
                nodes.append({
                    "text": "* " + title+" *",
                    "parent": parent,
                    "href": "javascript:nodeNameClick('%s')" % title,
                })
    except Exception as e:
        print(e)


def get_problems_by_source_title(source_title):
    _res_list = []
    _db = CommonDB()
    sql = "SELECT id,ojname FROM sourcetreeref WHERE source=%s"
    _db.execute(sql, (source_title,))
    _problems = _db.fetchall()
    _db.close()
    for _problem in _problems:
        _t_problem = {
            "id": _problem[0],
            "ojname": _problem[1]
        }
        _res_list.append(_t_problem)
    return _res_list
    pass
