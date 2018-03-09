# coding: utf-8
from spider.stageone.main import spider_api_stageone
from spider.stagetwo.main import start_spider_stagetwo
OJ_LIST_SZK = ['poj', 'zoj', 'uvalive']
OJ_LIST_FC = ['ural', 'hust', 'hysbz', 'hdu', 'codeforces', 'uva', 'spoj', 'sgu']


def craw_problem(oj_name, problem_id):
    msg = None
    if str(oj_name).lower() in OJ_LIST_SZK:
        msg = spider_api_stageone.craw_problem(oj_name=oj_name, problem_id=problem_id)
    elif str(oj_name).lower() in OJ_LIST_FC:
        msg = start_spider_stagetwo.craw_problem_by_id(oj_name=oj_name, problem_id=problem_id)
    return msg
    pass
