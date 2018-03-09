# coding: utf-8
from spider.stageone.db.db_operations import get_sources
from knowledge_tree.db.common_db import CommonDB
from source_tree.Trie import TrieTree
# import source_tree.db.db_operations
import time
import re
import os
# OJ列表
ojList = []
# 词典Trie
dictTrie =  TrieTree()
# 目录结构表
G = {}
# 命名实体种类
Type = {}
# 默认词典位置
defaultLoc = "./"
# 默认词典
defaultDict = ['ChinaUniversity', 'City', 'Country', 'Continent', 'OJ', 'Custom']

def init():
    G.clear()
    createDictTree()
    createSQLTable()
    pass

# 创建SoucreTree相关表
def createSQLTable():
    db_hundler = CommonDB()
    db_hundler.execute('create table if not exists sourcetreeref(source VARCHAR(200) PRIMARY KEY,\
                        level VARCHAR (100), date VARCHAR (20) ,parent VARCHAR (100), isUser INT)')
    db_hundler.execute('create table if not exists sourcetree(name VARCHAR(100) PRIMARY KEY, parent VARCHAR (100), \
                        needShow INT, haveProblem INT,theType VARCHAR (100))')
    for entry in G:
        db_hundler.execute("SELECT * FROM sourcetree WHERE name = %s", (entry))
        res = db_hundler.fetchall()
        if len(res) == 0:
            # 如果数据库中不存在该词条，则插入该词条
            db_hundler.execute("INSERT INTO sourcetree(name,parent,needShow,haveProblem,theType) \
                               VALUES(%s, %s, %s, %s, %s)",(entry, G[entry][0],G[entry][1],G[entry][2],Type[entry]))
        else:
            db_hundler.execute("UPDATE sourcetree SET needShow = %s, haveProblem = %s, theType = %s\
                WHERE name = %s AND parent = %s", (G[entry][1], G[entry][2], Type[entry], entry, G[entry][0]))

    db_hundler.commit()
    db_hundler.close()
    pass

def createDictTree():
    # 词典格式 node(node0,node1,node2,...) : parent
    # 加载中国大学名称词典
    db_hundler = CommonDB()
    try:
        db_hundler.execute("SELECT * FROM chinauniversity")
        res = db_hundler.fetchall()
        for entry in res:
            name = entry[0]
            parent = entry[1]
            abbr = entry[2]
            G[name] = [parent, 0, 0]
            Type[name] = 'chinauniversity'
            dictTrie.add(name)
            if abbr != "":
                dictTrie.add(abbr,name)
    except Exception as e:
        print(e)
    db_hundler.commit()
    db_hundler.close()
    # 加载城市名称词典
    db_hundler = CommonDB()
    try:
        db_hundler.execute("SELECT * FROM city")
        res = db_hundler.fetchall()
        for entry in res:
            name = entry[0]
            parent = entry[1]
            abbr = entry[2]
            G[name] = [parent, 0, 0]
            Type[name] = 'city'
            dictTrie.add(name)
            if abbr != "":
                dictTrie.add(abbr,name)
    except Exception as e:
        print(e)
    db_hundler.commit()
    db_hundler.close()
    # 加载国家名称词典
    db_hundler = CommonDB()
    try:
        db_hundler.execute("SELECT * FROM country")
        res = db_hundler.fetchall()
        for entry in res:
            name = entry[0]
            parent = entry[1]
            abbr = entry[2]
            G[name] = [parent, 1, 0]
            Type[name] = 'country'
            dictTrie.add(name)
            if abbr != "":
                dictTrie.add(abbr,name)
    except Exception as e:
        print(e)
    db_hundler.commit()
    db_hundler.close()
    # 加载大洲名称词典
    db_hundler = CommonDB()
    try:
        db_hundler.execute("SELECT * FROM continent")
        res = db_hundler.fetchall()
        for entry in res:
            name = entry[0]
            parent = entry[1]
            abbr = entry[2]
            G[name] = [parent, 1, 0]
            Type[name] = 'continent'
            dictTrie.add(name)
            if abbr != "":
                dictTrie.add(abbr,name)
    except Exception as e:
        print(e)
    db_hundler.commit()
    db_hundler.close()
    # 加载OJ词典
    db_hundler = CommonDB()
    try:
        db_hundler.execute("SELECT * FROM oj")
        res = db_hundler.fetchall()
        for entry in res:
            name = entry[0]
            parent = entry[1]
            abbr = entry[2]
            G[name] = [parent, 0, 0]
            Type[name] = 'oj'
            dictTrie.add(name)
            if abbr != "":
                dictTrie.add(abbr,name)
            ojList.append(name)
    except Exception as e:
        print(e)
    db_hundler.commit()
    db_hundler.close()
    # 加载自定义词典
    db_hundler = CommonDB()
    try:
        db_hundler.execute("SELECT * FROM custom")
        res = db_hundler.fetchall()
        for entry in res:
            name = entry[0]
            parent = entry[1]
            abbr = entry[2]
            G[name] = [parent, 1, 0]
            Type[name] = 'custom'
            dictTrie.add(name)
            if abbr != "":
                dictTrie.add(abbr,name)
    except Exception as e:
        print(e)
    db_hundler.commit()
    db_hundler.close()
    pass


def loadDefaultDict():
    for item in defaultDict:
        db_hundler = CommonDB()
        db_hundler.execute('create table if not exists '+item+'(name VARCHAR(100) PRIMARY KEY,\
            parent VARCHAR (100),abbr VARCHAR (100))')
        db_hundler.commit()
        db_hundler.close()
        with open(defaultLoc + item + '.txt', 'r') as f:
            for line in f:
                temp = line.rstrip('\n').split(' : ')
                name = temp[0]
                parent = temp[1]
                abbr = ""
                if len(temp) == 3:
                    abbr = temp[2]
                db_hundler = CommonDB()
                db_hundler.execute('SELECT * FROM '+item+' WHERE name = %s', (name))
                res = db_hundler.fetchone()
                if isinstance(res, tuple):
                    db_hundler.execute("UPDATE " + item + " SET parent = %s, abbr = %s WHERE name = %s",
                                       (parent, abbr, name))
                else:
                    db_hundler.execute("INSERT INTO "+item+"(name, parent, abbr) VALUES(%s, %s, %s)",
                                       (name, parent, abbr))
                db_hundler.commit()
                db_hundler.close()
    pass


# 获取目录结构
def getDictionary():
    # dict = {}
    # for item in G:
    #     parent = G[item][0]
    #     if parent not in dict:
    #         dict[parent] = [item]
    #     else:
    #         dict[parent].append(item)
    # print(dict)
    return G


def addKeyWord(ls, key):
    for item in key:
        if len(item) > 0 and item not in ls:
            ls.add(item)
    pass


# 生成目录路径
def processPath(name, tempDict):
    orignName = name
    ret = [name]
    while name != 'Root':
        if name in tempDict:
            ret += tempDict[name][1:]
            name = 'Root'
            break
        elif name in G:
            name = G[name][0]
            ret.append(name)
        else:
            break
    if name == 'Root':
        tempDict[orignName] = ret
    return ret

def defType(desc):
    type = 'Unknown'
    if len(re.findall('Region|NWERC|NEERC|SWERC|SEERC|CERC', desc, re.IGNORECASE)) > 0:
        type = 'Regional'
    elif len(re.findall('Provincial|Province', desc, re.IGNORECASE)) > 0:
        type = 'Provincial'
    elif len(re.findall('University', desc, re.IGNORECASE)) > 0:
        type = 'University\'s'
    else:
        for oj in ojList:
            if desc.count(oj) > 0:
                type = 'OJ\'s'
                break
    return type

# 生成唯一目录
def processDict(entry, oldSource, newSource, year='none'):
    tempDict = {}
    maxLen = 0
    path = []
    for item in entry :
        ret = processPath(item, tempDict)
        if len(ret) > maxLen:
            path = ret
            maxLen = len(ret)
    if len(path) == 0:
        path.append('Unknown')
    type = defType(newSource)
    #找到挂载点
    customAnthor = 'Root'
    for item in path:
        if item == 'Root' or item == 'Unknown':
            continue
        if G[item][1] == 1:
            G[item][2] = G[item][2] + 1
            if customAnthor == 'Root':
                customAnthor = item
    # 连接数据库
    db_hundler = CommonDB()
    # 更新映射表
    db_hundler.execute("SELECT * FROM sourcetreeref WHERE source = %s", (oldSource))
    isExist = len(db_hundler.fetchall()) > 0
    if isExist:
        db_hundler.execute("UPDATE sourcetreeref SET level = %s, date = %s, parent = %s, isUser = %s \
        WHERE source = %s", (type, year, customAnthor, 0,oldSource))
    else:
        db_hundler.execute("INSERT INTO sourcetreeref(source,level,date,parent,isUser) \
        VALUES(%s, %s, %s, %s, %s)", (oldSource, type, year, customAnthor, 0))
    db_hundler.commit()
    #关闭数据库
    db_hundler.close()
    pass

def updateToSQL():
    # 连接数据库
    db_hundler = CommonDB()
    # 更新目录表
    for entry in G:
        db_hundler.execute("UPDATE sourcetree SET needShow = %s, haveProblem = %s WHERE name = %s",\
                        (G[entry][1],G[entry][2],entry))
    db_hundler.commit()
    db_hundler.close()

def simpleSource(source):
    if source is None or source == "":
        OldSource = 'Unkonwn'
    else:
        OldSource = ' ' + source
    OldSource = re.sub(r"<[^>]*>", "", OldSource)
    OldSource = re.sub(r"</[^>]*>", "", OldSource).strip()
    return OldSource

def match(sources):
    ret = set()
    for item in sources:
        # 匹配地区
        OldSource = simpleSource(item[0])
        newSource = ' '+re.sub(r'[^a-zA-z0-9]|Source', ' ', OldSource).strip()
        for index in re.finditer(r'\s+', newSource):
            addKeyWord(ret,dictTrie.match(newSource[index.end():]))
        # 匹配日期
        year = findYear(newSource)
        # 生成目录
        print(newSource)
        processDict(ret,OldSource,newSource,year)
        ret.clear()
    pass

def findYear(source):
    curYear = time.strftime('%Y', time.localtime())
    pattern = re.compile(r'\d{4}')
    for year in re.findall(pattern, source):
        if year <= curYear:
            return year
    return 'none'

def fixProblemCount(name, num):
    if name == 'Root':
        return
    G[name][2] = max(0, G[name][2] + num)
    fixProblemCount(G[name][0], num)
    pass
def restoreUserOp(sources, force = False):
    data = []
    try:
        db_hundler = CommonDB()
        for item in sources:
            OldSource = simpleSource(item[0])
            db_hundler.execute("SELECT * FROM sourcetreeref")
            res = db_hundler.fetchall()
            needRemove = False
            for entry in res:
                tempSource = simpleSource(entry[0])
                parent = entry[3]
                isUser = int(entry[4])
                if tempSource == OldSource:
                    if isUser == 1 and force == False:
                        needRemove = True
                        fixProblemCount(parent, + 1)
                else:
                    fixProblemCount(parent, + 1)
            if needRemove == False:
                data.append(item)
    except Exception as e:
        print(e)
    db_hundler.close()
    return data

def updateProblem(id, ojname, force = False):
    data = {}
    try:
        source = get_sources(id, ojname, force)
        if len(source) == 0:
            data["res"] = "error"
            data["msg"] = ojname + " " + id + " 找不到题目"
            return data
        init()
        source = restoreUserOp(source, force)
        match(source)
        updateToSQL()
        data["res"] = "success"
        data["msg"] = ojname + " " + id + " 更新成功"
    except Exception as e:
        data["res"] = "error"
        data["msg"] = str(e)
    return data

def resetDict():
    pass

if __name__ == "__main__" :
    updateProblem(1100, 'Poj')
