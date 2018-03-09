import os

from django.contrib import admin

# Register your models here.
from mixojapp.models import Problem
from mixojapp.models import ProblemStatus, OJ

admin.site.register(Problem)
admin.site.register(ProblemStatus)
admin.site.register(OJ)


# import os
# import sys
# pathname = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, pathname)
# sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
# sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../..')))
#
# # 如果没有设置 DJANGO_SETTINGS_MODULE, 则设置
# if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
#     import django
#
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mixoj.settings")
#     django.setup()
# # end
#
# from mixojapp.models import OJ, Problem


# 维护OJ名的表
OJ_LIST = ["Poj", "Zoj", "UVALive", "Sgu", 'Ural', 'Hust', 'Hysbz', 'Hdu', 'Codeforces', 'UVA']


def update_oj_table():
    exists_ojs = OJ.objects.all()
    for exists_oj in exists_ojs:
        exists_oj.delete()

    exists_ojs_set = set()
    for oj in OJ_LIST:
        exists_ojs_set.add(oj)
        new_oj = OJ(name=oj)
        new_oj.save()

    ojnames = Problem.objects.only("ojname")
    for ojname in ojnames:
        if ojname.ojname not in exists_ojs_set:
            new_oj = OJ(name=ojname.ojname)
            exists_ojs_set.add(ojname.ojname)
            new_oj.save()
            pass


def update_hot_and_difficult_degree():
    from spider.stagetwo.main.degree import degree as figure_degree
    for oj in OJ_LIST:
        try:
            figure_degree(oj)
            pass
        except:
            pass
    pass


try:
    update_oj_table()
    update_hot_and_difficult_degree()
except:
    pass
