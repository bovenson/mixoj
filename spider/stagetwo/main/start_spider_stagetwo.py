from spider.stagetwo.main.main_spider import OjSpider
from mixojapp.models import SpojProblem

OJ_LIST_SZK = ['poj', 'zoj', 'sgu', 'uvalive', 'ural', 'hust', 'hdu', 'hysbz', 'codeforces', 'uva', 'spoj']


def craw_problem_by_id(oj_name, problem_id):
    reses = []
    msges = []
    if str(oj_name).lower() in OJ_LIST_SZK:
        if str(oj_name).lower() == 'codeforces':
            i = 65
            while i < 70:
                problem_ids = str(problem_id) + "/" + str(chr(i))
                msg = craw_problem(oj_name=oj_name, problem_id=problem_ids)
                msges.append(msg.get("msg"))
                reses.append(msg.get("res"))
                i += 1
        else:
            msg = craw_problem(oj_name=oj_name, problem_id=problem_id)
            msges.append(msg.get("msg"))
            reses.append(msg.get("res"))
    return {"res": reses, "msg": ",".join(msges)}
    pass


def craw_problem(oj_name, problem_id):
    _res = {}
    try:
        url = get_url_by_id(oj_name, problem_id)
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


def get_url_by_id(ojname, problem_id):
    oj_name = str(ojname).lower()
    url = ""
    # if oj_name == "poj":
    #     url = "http://poj.org/problem?id=" + str(problem_id)
    # elif oj_name == "uvalive":
    #     url = "https://icpcarchive.ecs.baylor.edu/index.php?" \
    #           "option=com_onlinejudge&Itemid=8&category=&page=show_problem&problem=%s" + str(problem_id)
    if oj_name == "sgu":
        url = "http://acm.sgu.ru/problem.php?contest=0&problem=" + str(problem_id)
    # elif oj_name == "zoj":
    #     url = "http://acm.zju.edu.cn/onlinejudge/showProblem.do?problemCode=" + str(problem_id)
    elif oj_name == "ural":
        url = "http://acm.timus.ru/problem.aspx?space=1&num=" + str(problem_id)
    elif oj_name == "hust":
        url = "http://acm.hust.edu.cn/problem/show/" + str(problem_id)
    elif oj_name == "hysbz":
        url = "http://www.lydsy.com/JudgeOnline/problem.php?id=" + str(problem_id)
    elif oj_name == "hdu":
        url = "http://acm.hdu.edu.cn/showproblem.php?pid=" + str(problem_id)
    elif oj_name == "codeforces":
        url = "http://codeforces.com/problemset/problem/" + str(problem_id)
    elif oj_name == "uva":
        url = "https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=&" \
              "page=show_problem&problem=" + str(problem_id)
    elif oj_name == "spoj":
        spoj_problem = SpojProblem.objects.get(sourceid=problem_id)
        url = spoj_problem.url
    return url


if __name__ == "__main__":
    craw_problem_by_id('codeforces', 30)
