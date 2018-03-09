# coding: utf-8

# 使用 Django 模型实现数据存储
import os
import sys
import math
import re
import random

pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../..')))

# 如果没有设置 DJANGO_SETTINGS_MODULE, 则设置
if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mixoj.settings")
    django.setup()
# end
from mixojapp.models import ProblemStatus, Problem, ProblemDegree


def calculat_oj(oj_name):
    problems = Problem.objects.filter(ojname=oj_name)
    nums = []
    sum_sub = 0
    sum_num = 0
    sum_ac = 0
    numss = []
    for i in problems:
        if i.ac_rate is not None:
            nums = re.compile(r"\d+").findall(i.ac_rate)
            real_ac_rate = int(nums[0]) + int(nums[1]) * 0.01
            sum_ac = sum_ac + real_ac_rate
            sum_num = sum_num + 1
            numss.append(real_ac_rate)

    if sum_ac != 0:
        dif_average_ac = sum_ac / sum_num
    else:
        dif_average_ac = 0
    sum_sqrt = 0
    for i in numss:
        sum_sqrt = sum_sqrt + (i - dif_average_ac) ** 2
    if sum_sqrt != 0:
        dif_average_sqrt = math.sqrt(sum_sqrt / sum_num)
    else:
        dif_average_sqrt = 0

    for i in problems:
        try:
            problem_status = ProblemStatus.objects.get(problem=i)
            if problem_status.total_sub is not None:
                sum_sub = sum_sub + int(problem_status.total_sub)
                sum_num = sum_num + 1
                nums.append(int(problem_status.total_sub))
        except:
            pass
    if sum_sub != 0:
        average_sub = sum_sub / sum_num
    else:
        average_sub = 0
    sum_squr = 0
    for i in nums:
        sum_squr = sum_squr + (int(i) - average_sub) ** 2
    if sum_sqrt != 0:
        average_squr = math.sqrt(sum_squr / sum_num)
    else:
        average_squr = 0
    problem_degree = ProblemDegree.objects.filter(ojname=oj_name)
    if len(problem_degree) == 0:
        res = ProblemDegree(ojname=oj_name, hot_average_sub=average_sub, hot_average_sqrt=average_squr,
                            dif_average_ac=dif_average_ac, difaverage_sqrt=dif_average_sqrt)

        res.save()
    else:
        a = problem_degree[0]
        a.dif_average_ac = dif_average_ac
        a.hot_average_sub = average_sub
        a.hot_average_sqrt = average_squr
        a.difaverage_sqrt = dif_average_sqrt
        a.save()


def analyse_hot_degree(oj_name):
    res = ProblemDegree.objects.filter(ojname=oj_name)
    if len(res) == 0:
        calculat_oj(oj_name)
        res = ProblemDegree.objects.filter(ojname=oj_name)
    data = res[0]
    average_sub = data.hot_average_sqrt
    average_squr = data.hot_average_sqrt
    problems = Problem.objects.filter(ojname=oj_name)
    for i in problems:
        try:
            problem_status = ProblemStatus.objects.get(problem=i)
            x = problem_status.total_sub
            res = (int(x) - average_sub) / average_squr
            i.hot_degree = res
            i.save()
        except:
            pass
    pass


def analyse_difficult_degree(oj_name):
    res = ProblemDegree.objects.filter(ojname=oj_name)
    if len(res) == 0:
        calculat_oj(oj_name)
        res = ProblemDegree.objects.filter(ojname=oj_name)
    data = res[0]
    average_ac = data.dif_average_ac
    average_sqrt = data.difaverage_sqrt
    problems = Problem.objects.filter(ojname=oj_name)
    for i in problems:
        if i.ac_rate is not None:
            nums = re.compile(r"\d+").findall(i.ac_rate)
            real_ac_rate = int(nums[0]) + int(nums[1]) * 0.01
            hehe = (real_ac_rate - average_ac) / average_sqrt
            i.difficult = hehe
            i.save()

    pass


def degree(oj_name):
    calculat_oj(oj_name)
    analyse_hot_degree(oj_name)
    analyse_difficult_degree(oj_name)


if __name__ == "__main__":
    # calculat_oj('Zoj')
    # analyse_hot_degree('Zoj')
    # analyse_difficult_degree("Zoj")
    degree("Hust")
    pass
