from collections import OrderedDict

import time
from django.db import models


# Create your models here.


class Problem(models.Model):
    """题目Model"""
    # 题目在数据库中的id
    id = models.AutoField(primary_key=True)
    # 题目源url
    url = models.CharField(max_length=150, unique=True, null=False, blank=False)
    # 题目在源oj中的id
    sourceid = models.CharField(max_length=20, null=True, default="")
    # 题目所属OJ的名称
    ojname = models.CharField(max_length=30, default="")
    # 时间限制
    time_limit = models.CharField(max_length=20, null=True)
    # 内存限制
    memory_limit = models.CharField(max_length=20, null=True)
    # 题目名称
    title = models.TextField(max_length=200, default="")
    # 题目描述
    description = models.TextField(max_length=100000, null=True)
    # 题目输入
    pinput = models.TextField(max_length=100000, null=True)
    # 题目输出
    poutput = models.TextField(max_length=100000, null=True)
    # 样例输入
    sample_input = models.TextField(max_length=100000, null=True)
    # 样例输出
    sample_output = models.TextField(max_length=100000, null=True)
    # 提示
    hint = models.TextField(max_length=100000, null=True)
    # 来源
    source = models.TextField(max_length=200, null=True)
    # AC 率
    ac_rate = models.CharField(max_length=10, null=True)
    # 用户 AC 率
    user_ac_rate = models.CharField(max_length=10, null=True)
    # update time
    update_time = models.DateTimeField(auto_now=True, null=True)
    # knowledge tree node id
    knowledge_tree_node_id = models.IntegerField(default="-1")
    # knowledge tree node name
    knowledge_tree_node_name = models.CharField(max_length=30, default="未分类")

    hot_degree = models.FloatField(max_length=20, null=True)
    difficult = models.FloatField(max_length=20, null=True)

    def __str__(self):
        return str(self.id) + " " + str(self.title)

    pass


# 题目数据
class ProblemStatus(models.Model):
    """题目数据Model"""
    id = models.AutoField(primary_key=True)
    # 总提交数
    total_sub = models.CharField(max_length=8, null=True)
    # 尝试提交的用户数
    user_sub = models.CharField(max_length=8, null=True)
    # 解决该问题的用户数
    user_ac = models.CharField(max_length=8, null=True)
    # AC 次数
    ac = models.CharField(max_length=8, null=True)
    # presentation error
    pe = models.CharField(max_length=8, null=True)
    # time limit exceeded
    tle = models.CharField(max_length=8, null=True)
    # memory limit exceeded
    mle = models.CharField(max_length=8, null=True)
    # wrong answer
    wa = models.CharField(max_length=8, null=True)
    # runtime error
    re = models.CharField(max_length=8, null=True)
    # output limit exceeded
    ole = models.CharField(max_length=8, null=True)
    # compile error
    ce = models.CharField(max_length=8, null=True)
    # system error
    se = models.CharField(max_length=8, null=True)
    # waiting
    waiting = models.CharField(max_length=8, null=True)
    # Floating Point Error
    fpe = models.CharField(max_length=8, null=True)
    # Segmentation Fault
    sf = models.CharField(max_length=8, null=True)
    # Non-zero Exit Code
    nzec = models.CharField(max_length=8, null=True)
    # 设置外键
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE, null=True, blank=True)

    def get_statistics(self):
        data = OrderedDict()
        if self.total_sub is not None:
            data["Total Submissions"] = self.total_sub
        if self.user_sub is not None:
            data["Users(Submitted)"] = self.user_sub
        if self.user_ac is not None:
            data["Users(Solved)"] = self.user_ac
        if self.ac is not None:
            data["Accepted"] = self.ac
        if self.pe is not None:
            data["Presentation Error"] = self.pe
        if self.tle is not None:
            data["Time Limit Exceeded"] = self.tle
        if self.mle is not None:
            data["Memory Limit Exceeded"] = self.mle
        if self.wa is not None:
            data["Wrong Answer"] = self.wa
        if self.re is not None:
            data["Runtime Error"] = self.re
        if self.ole is not None:
            data["Output Limit Exceeded"] = self.ole
        if self.ce is not None:
            data["Compile Error"] = self.ce
        if self.se is not None:
            data["System Error"] = self.se
        if self.fpe is not None:
            data["Floating Point Error"] = self.fpe
        if self.sf is not None:
            data["Segmentation Fault"] = self.sf
        if self.nzec is not None:
            data["Non-zero Exit Code"] = self.nzec

        # fields = self._meta.get_fields()
        # for field in fields:
        #     field = str(field).split(".")[-1]
        #     get_val = getattr(self, field)
        #     if get_val is not None:
        #         data[field] = get_val
        return data

    def __str__(self):
        return self.problem.title

    pass


class OJ(models.Model):
    name = models.CharField(max_length=100)
    id_start = models.CharField(max_length=100, default=0)
    id_end = models.CharField(max_length=100, default=0)
    pass


class ProblemDegree(models.Model):
    ojname = models.CharField(max_length=30, default="")
    hot_average_sub = models.FloatField(max_length=20, default=0)
    hot_average_sqrt = models.FloatField(max_length=20, default=0)
    dif_average_ac = models.FloatField(max_length=20, default=0)
    difaverage_sqrt = models.FloatField(max_length=20, default=0)

    def __str__(self):
        return self.ojname


class SpojProblem(models.Model):
    url=models.CharField(max_length=100, default="")
    sourceid = models.CharField(max_length=20, null=True, default="",unique=True)