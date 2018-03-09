# coding: utf-8
from spider.stageone.main.main_spider import OjSpider
from spider.stageone.public.str_process import str_is_equal_ignore_case

BASE_URL_UVALIVE= "https://icpcarchive.ecs.baylor.edu/index.php?" \
                  "option=com_onlinejudge&Itemid=8&category=&page=show_problem&problem=%s"
BASE_URL_POJ = "http://poj.org/problem?id=%s"
BASE_URL_ZOJ = "http://acm.zju.edu.cn/onlinejudge/showProblem.do?problemCode=%s"
BASE_URL_SGU = "http://acm.sgu.ru/problem.php?contest=0&problem=%s"


def get_url_by_id(oj_name, problem_id):
    if str_is_equal_ignore_case(oj_name, "uvalive"):
        return BASE_URL_UVALIVE % (str(problem_id),)
    elif str_is_equal_ignore_case(oj_name, "poj"):
        return BASE_URL_POJ % (str(problem_id),)
    elif str_is_equal_ignore_case(oj_name, "zoj"):
        return BASE_URL_ZOJ % (str(problem_id),)
    elif str_is_equal_ignore_case(oj_name, "sgu"):
        return BASE_URL_SGU % (str(problem_id),)
    pass


# def craw_one_problem(oj_name, problem_id):
#     """给出一个OJ名及所在oj的id,爬取该题目"""
#     url = get_url_by_id(oj_name=oj_name, problem_id=problem_id)
#     OjSpider.runspider(oj_name=oj_name, root_url=url, page_to_craw=1, operation=FIRST_CRAW)
#     pass
#
#
# def update_one_problem(oj_name, problem_id):
#     """给出一个OJ名及所在oj的id,更新该题目"""
#     url = get_url_by_id(oj_name=oj_name, problem_id=problem_id)
#     OjSpider.runspider(oj_name=oj_name, root_url=url, page_to_craw=1, operation=UPDATE)
#     pass


# def craw_problems(oj_name, start_id, end_id):
#     _data = {}
#     try:
#         start_id = int(start_id)
#         end_id = int(end_id)
#         while 0 <= start_id <= end_id:
#             craw_one_problem(oj_name=oj_name, problem_id=start_id)
#             pass
#         pass
#     except:
#         _data["res"] = "error"
#         _data["res"] = "抓取时出错"
#         pass
#     else:
#         _data["res"] = "success"
#         _data["res"] = "抓取成功"
#     return _data
#     pass
#
#
# def update_problems(oj_name, start_id, end_id):
#     _data = {}
#     try:
#         start_id = int(start_id)
#         end_id = int(end_id)
#         while 0 <= start_id <= end_id:
#             update_one_problem(oj_name=oj_name, problem_id=start_id)
#             pass
#         pass
#     except:
#         _data["res"] = "error"
#         _data["res"] = "抓取时出错"
#         pass
#     else:
#         _data["res"] = "success"
#         _data["res"] = "抓取成功"
#     return _data
#     pass


def craw_problem(oj_name, problem_id):
    _res = {}
    try:
        url = get_url_by_id(oj_name=oj_name, problem_id=problem_id)
        # print("Craw:", url)
        _craw_res = OjSpider.craw_one_page(oj_name=oj_name, problem_id=problem_id, cur_url=url)
        _res["res"] = _craw_res.get("res")
        _res["msg"] = "爬取 " + str(oj_name) + " " + str(problem_id) + " " + _craw_res.get("msg")
        pass
    except Exception as e:
        import traceback
        traceback.print_exc()
        _res["res"] = "error"
        _res["msg"] = "爬取 " + str(oj_name) + " " + str(problem_id) + " 时出错:" + str(e)
        pass
    else:
        if _res.get("res") is None:
            _res["res"] = "success"
            _res["msg"] = "爬取 " + str(oj_name) + " " + str(problem_id) + " 成功"
        pass
    pass
    return _res

if __name__ == "__main__":
    # craw_one_problem(oj_name="poj", problem_id="1037")
    # craw_problem("Poj", "10123")
    print(get_url_by_id("UvaLive", "5576"))
    pass
