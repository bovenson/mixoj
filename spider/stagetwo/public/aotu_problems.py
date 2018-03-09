import re
import os
import sys
import random
from knowledge_tree.db.common_db import CommonDB

DB_TABLE_NAME = "knowledge_tree"
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../..')))
if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mixoj.settings")
    django.setup()
from  mixojapp.models import Problem

names = []


def aotu_problems(ojname="All", dif_degrees="All", hot_degrees="All", knowledge="All", nums="0"):
    if ojname is None or ojname == "All":
        oj_name = ""
    else:
        oj_name = ojname
    if knowledge is None or  knowledge == "All":
        know = ""
    else:
        know = knowledge
    if dif_degrees is None or dif_degrees == "All":
        dif_degree = 0
    else:
        dif_degree = int(dif_degrees)
    if hot_degrees is None or hot_degrees == "All":
        hot_degree = 0
    else:
        hot_degree = int(hot_degrees)
    if nums is None or nums == "0":
        num = 0
    else:
        num = int(nums)
    print(hot_degree, dif_degree, num, know, oj_name)
    problems = []
    if oj_name == "":
        problemlist = Problem.objects.all()
        if dif_degree == 0:
            if hot_degree == 0:
                if know == "":
                    names = get_knowledge_name()
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
                    pass
                else:
                    names=[]
                    names = get_chid_by_name(know,names)
                    print(names)
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)

                pass
            else:
                hot_one = -2.5 + 1 * (hot_degree - 1)
                hot_two = -1.5 + 1 * (hot_degree - 1)
                problemlist = problemlist.filter(hot_degree__range=(hot_one, hot_two))
                if know == "":
                    names = get_knowledge_name()

                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
                    pass
                else:
                    names=[]
                    names = get_chid_by_name(know,names)
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
            pass
        else:
            dif_one = -2.5 + 1 * (dif_degree - 1)
            dif_two = -1.5 + 1 * (dif_degree - 1)
            problemlist = problemlist.filter(difficult__range=(dif_one, dif_two))
            if hot_degree == 0:
                if know == "":
                    names = get_knowledge_name()
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
                    pass
                else:
                    names=[]
                    names = get_chid_by_name(know,names)
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
                pass
            else:
                hot_one = -2.5 + 1 * (hot_degree - 1)
                hot_two = -1.5 + 1 * (hot_degree - 1)
                problemlist = problemlist.filter(hot_degree__range=(hot_one, hot_two))
                if know == "":
                    names = get_knowledge_name()
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
                    pass
                else:
                    names=[]
                    names = get_chid_by_name(know,names)
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
    else:
        problemlist = Problem.objects.filter(ojname=oj_name)
        if dif_degree == 0:
            if hot_degree == 0:
                if know == "":
                    names = get_knowledge_name()
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
                    pass
                else:
                    names=[]
                    names = get_chid_by_name(know,names)
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
                pass
            else:
                hot_one = -2.5 + 1 * (hot_degree - 1)
                hot_two = -1.5 + 1 * (hot_degree - 1)
                problemlist = problemlist.filter(hot_degree__range=(hot_one, hot_two))
                if know == "":
                    names = get_knowledge_name()
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
                    pass
                else:
                    names=[]
                    names = get_chid_by_name(know,names)
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
            pass
        else:
            dif_one = -2.5 + 1 * (dif_degree - 1)
            dif_two = -1.5 + 1 * (dif_degree - 1)
            problemlist = problemlist.filter(difficult__range=(dif_one, dif_two))
            if hot_degree == 0:
                if know == "":
                    names = get_knowledge_name()
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
                    pass
                else:
                    names=[]
                    names = get_chid_by_name(know,names)
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
                pass
            else:
                hot_one = -2.5 + 1 * (hot_degree - 1)
                hot_two = -1.5 + 1 * (hot_degree - 1)
                problemlist = problemlist.filter(hot_degree__range=(hot_one, hot_two))
                if know == "":
                    names = get_knowledge_name()
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
                    pass
                else:
                    names=[]
                    names = get_chid_by_name(know,names)
                    problems = add_problems_all(num=num, problemlist=problemlist, names=names)
    print(problems)
    names = []
    return problems
    pass


def add_problem(num, problemlist, name):
    problems = []
    list_len = len(problemlist)
    if num > list_len:
        num = list_len
    while num > 0:
        if list_len > 0:
            index = random.randint(0, list_len - 1)
            if problemlist[index] in problems:
                pass
            else:
                problems.append(problemlist[index])
                num = num - 1
    return problems


def get_chid_by_name(name,names):
    names.append(name)
    _db = CommonDB()
    sql = "SELECT id FROM " + DB_TABLE_NAME + " WHERE name=%s"
    try:
        _db.execute(sql, (name))
        _result = _db.fetchone()
        if _result is not None:
            id = _result[0]
            print()
            sql = "SELECT name FROM " + DB_TABLE_NAME + " WHERE pid=%s"
            _db.execute(sql, (id))
            _results = _db.fetchall()
            if _results is not None:
                for i in _results:
                    get_chid_by_name(i[0],names)
        else:
            print("无此节点")
    except Exception as e:
        print("查询知识树结构时出错: ", e)
        pass
    return names


def add_problems_all(num, problemlist, names):
    count=0
    problems = []
    names_len = len(names)
    list_len = len(problemlist)
    total=0
    for name in names:
        total=total+len(problemlist.filter(knowledge_tree_node_name=name))
    print(total)
    if num>total:
        num=total
    print(list_len)
    if num > list_len:
        num = list_len
    print(num)
    while num > 0:
      if count>20:
         break
      if len(names)>0:
        print(num)
        index = random.randint(0, names_len - 1)
        name = names[index]
        print(name)
        nameslist = problemlist.filter(knowledge_tree_node_name=name)
        list_len = len(nameslist)
        if list_len==0:
            names.remove(name)
            names_len=names_len-1
        if list_len > 0:
            index = random.randint(0, list_len - 1)
            if nameslist[index] in problems:
                count=count+1
                pass
            else:
                problems.append(nameslist[index])
                num = num - 1
        else:
            count=count+1
      else:
          break
    return problems


def get_knowledge_name():
    _db = CommonDB()
    names = []
    sql = "SELECT name FROM " + DB_TABLE_NAME
    try:
        _db.execute(sql)
        for item in _db.fetchall():
            names.append(item[0])
    except Exception as e:
        print("查询知识树结构时出错: ", e)
    return names


if __name__ == "__main__":
    aotu_problems(ojname="All",dif_degrees="All",hot_degrees="All",knowledge="最长路",nums="5")
    #aotu_problems(ojname="All",dif_degrees="All",hot_degrees="All",knowledge="All",nums="5")
