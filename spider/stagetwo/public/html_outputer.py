# coding: utf-8

# 使用 Django 模型实现数据存储
import os
import sys

import re

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
from mixojapp.models import ProblemStatus, Problem

FIRST_CRAW = 1
UPDATE = 2


class HtmlOutputer(object):
    """保存爬取到的数据"""

    @staticmethod
    def save_to_db_auto(ojname, problem_id, problem, statistic):
        if ojname == "codeforces":
            strs = re.split(re.compile(r"/"), problem_id)
            problem_id = strs[0] + strs[1]

        problems = Problem.objects.filter(ojname=ojname, sourceid=problem_id)
        if len(problems) == 0:
            HtmlOutputer.save_to_db(problem, statistic, FIRST_CRAW)
        else:
            HtmlOutputer.save_to_db(problem, statistic, UPDATE)
        pass

    @staticmethod
    def save_to_db(problem, statistic, operation=FIRST_CRAW):
        # 判断插入题目数据条件

        if problem is None or problem.get('description') is None or len(problem) < 2:
            return
        # 计算 AC 率
        if statistic is not None and statistic.get("total_sub") is not None:
            if statistic.get("total_sub") is not None and statistic.get("ac") is not None:
                if int(statistic.get("total_sub")) != 0:
                    ac_rate = float(statistic.get("ac")) / float(statistic.get("total_sub"))
                    ac_rate = str("%.2f%%" % (ac_rate * 100))
                    problem["ac_rate"] = ac_rate
        # 计算用户 AC 率
        if statistic is not None and statistic.get("total_sub") is not None:
            if statistic.get("user_sub") is not None and statistic.get("user_ac") is not None:
                if int(statistic.get("user_sub")) != 0:
                    user_ac_rate = float(statistic.get("user_ac")) / float(statistic.get("user_sub"))
                    user_ac_rate = str("%.2f%%" % (user_ac_rate * 100))
                    problem["user_ac_rate"] = user_ac_rate
        # _search_content=problem["ojname"]+problem["sourceid"]
        # knowledge=runknowledgetree(_search_content)
        # problem["knowledge"]=knowledge
        # source={}
        # source["source"]=problem["source"]
        # source["title"]=problem["title"]
        # source["url"]=problem["url"]
        # update(source)
        # 保存问题
        new_problem = HtmlOutputer.save_problem_to_db(problem, operation=operation)
        if new_problem is not None and statistic is not None:
            statistic['problem'] = new_problem
            HtmlOutputer.save_statistic_to_db(statistic, operation=operation)
        pass

    # 保存题目
    @staticmethod
    def save_problem_to_db(problem_data, operation=FIRST_CRAW):
        # 判断插入题目数据条件
        if problem_data is None or problem_data.get('description') is None or len(problem_data) < 2:
            # print("插入失败")
            return
        new_problem = None
        if operation == UPDATE:
            try:
                new_problem = Problem.objects.get(url__iexact=problem_data.get('url'))
                HtmlOutputer.set_problem(new_problem, problem_data)
                new_problem.save()
            except Exception as e:
                print("更新题目,查询时出错:", e)
                pass
            pass
        else:
            new_problem = Problem()
            HtmlOutputer.set_problem(new_problem, problem_data)
            new_problem.save()
        return new_problem
        pass

    @staticmethod
    def save_statistic_to_db(statistics_data, operation=FIRST_CRAW):
        if statistics_data is None or len(statistics_data) < 1:
            return
        # print(statistics_data.get("problem").id)

        if operation == UPDATE:
            # print(statistics_data.get("problem"))
            # print("更新数据")
            new_status = ProblemStatus.objects.get(problem=statistics_data.get("problem"))
            HtmlOutputer.set_statistics(new_status, statistics_data)
            new_status.save()
        else:
            new_status = ProblemStatus()
            HtmlOutputer.set_statistics(new_status, statistics_data)
            new_status.save()
        pass

    @staticmethod
    def set_problem(problem, problem_data):
        problem.url = problem_data.get('url')
        problem.sourceid = problem_data.get('sourceid')
        problem.ojname = problem_data.get('ojname')
        problem.time_limit = problem_data.get('time_limit')
        problem.memory_limit = problem_data.get('memory_limit')
        problem.title = problem_data.get('title')
        problem.description = problem_data.get('description')
        problem.pinput = problem_data.get('pinput')
        problem.poutput = problem_data.get('poutput')
        problem.sample_input = problem_data.get('sample_input')
        problem.sample_output = problem_data.get('sample_output')
        problem.hint = problem_data.get('hint')
        problem.source = problem_data.get('source')
        problem.ac_rate = problem_data.get('ac_rate')
        problem.user_ac_rate = problem_data.get('user_ac_rate')
        # problem.knowledge = problem_data.get('knowledge')

    @staticmethod
    def set_statistics(new_status, statistics_data):
        new_status.total_sub = statistics_data.get('total_sub')
        new_status.user_sub = statistics_data.get('user_sub')
        new_status.user_ac = statistics_data.get('user_ac')
        new_status.ac = statistics_data.get('ac')
        new_status.pe = statistics_data.get('pe')
        new_status.tle = statistics_data.get('tle')
        new_status.mle = statistics_data.get('mle')
        new_status.wa = statistics_data.get('wa')
        new_status.re = statistics_data.get('re')
        new_status.ole = statistics_data.get('ole')
        new_status.ce = statistics_data.get('ce')
        new_status.se = statistics_data.get('se')
        new_status.waiting = statistics_data.get('waiting')
        new_status.fpe = statistics_data.get('fpe')
        new_status.sf = statistics_data.get('sf')
        new_status.nzec = statistics_data.get('nzec')
        new_status.problem = statistics_data.get('problem')
        pass

    pass


if __name__ == "__main__":
    # problem = Problem.objects.get(id=458)
    # status = ProblemStatus.objects.get(problem=problem)
    # print(status)
    pass
