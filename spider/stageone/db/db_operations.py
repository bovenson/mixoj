# codding: utf-8
# 使用 Django 模型实现数据存储
import os
import sys
from knowledge_tree.db.common_db import CommonDB
# 如果没有设置 DJANGO_SETTINGS_MODULE, 则设置
if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django
    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mixoj.settings")
    django.setup()
from mixojapp.models import Problem


def get_old_urls(oj_name):
    # 对 OJ 名判断
    if oj_name is None or str(oj_name) == "":
        return None
    que_res = Problem.objects.filter(ojname__iexact=oj_name).values('url')
    urls = []
    for url in que_res:
        urls.append(url.get('url'))
    return urls
    pass

def get_sources(id, oj_name, force = False):
    # 获得已抓取题目的source
    db_hundler = CommonDB()
    if oj_name == 'All':
        oj_name = '%'
    db_hundler.execute("SELECT source FROM mixojapp_problem "
                       "WHERE sourceid LIKE %s AND ojname LIKE %s",(id, oj_name))
    res = db_hundler.fetchall()
    db_hundler.close()
    sourceSet = []
    entry = []
    for item in res:
        for word in item:
            entry.append(word)
        sourceSet.append(entry.copy())
        entry.clear()
    return sourceSet
    pass

if __name__ == "__main__":
    print(get_old_urls("Poj"))
    pass
