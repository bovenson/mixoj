import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, JsonResponse
from django.shortcuts import render

from knowledge_tree.db.db_operations import get_all_knowledge_node_name
from mixojapp.admin import update_hot_and_difficult_degree
from source_tree.db.db_operations import get_problems_by_source_title
from spider.api import craw_problem as api_craw_problem
from mixojapp.models import Problem, ProblemStatus, OJ
from mixojapp.operations import update_problem_by_id
from spider.stagetwo.public.aotu_problems import aotu_problems


def problem_list(request, page=1):
    # 得到所有题目
    print(request.GET)
    problems = Problem.objects.all().order_by("id")
    # 跳转来源
    page_from = request.GET.get("page_from")
    node_id = request.GET.get("node_id")
    title = request.GET.get("title")
    # 分页
    # 每页记录数
    # problem_cnt_per_page = 30
    # problem_page_list = Paginator(problems, problem_cnt_per_page)
    # total_pages = problem_page_list.num_pages
    # try:
    #     problems_cur_page = problem_page_list.page(page)
    #     pass
    # except EmptyPage:
    #     problems_cur_page = problem_page_list.page(problem_page_list.num_pages)
    #     page = problem_page_list.num_pages
    #     pass
    # except:
    #     problems_cur_page = problem_page_list.page(1)
    #     page = 1
    #     pass
    # page = int(page)
    ojs = OJ.objects.all()
    data_cont = {
        "title": "Problem List",
        # "problems": problems_cur_page,
        # "page1st": page-2,
        # "page2ed": page-1,
        # "page3th": page,
        # "page4th": page+1 if page+1 <= total_pages else 0,
        # "page5th": page+2 if page+2 <= total_pages else 0,
        # "page_last": total_pages,
        "ojs": ojs,
        "page_from": page_from,
        "node_id": node_id,
        "source_title": title,
    }
    return render(request, "mixojapp/problemlist.html", data_cont)
    pass


def show_problem(request, problemid):
    hit_problem = Problem.objects.get(id=problemid)
    if hit_problem is None:
        raise Http404("题目不存在")
    data_cont = {
        "title": hit_problem.title,
        "problem": hit_problem,
    }
    return render(request, "mixojapp/problem.html", data_cont)
    pass


def show_statistics(request, problemid):
    try:
        problem = Problem.objects.get(id=problemid)
        hit_statistic = ProblemStatus.objects.get(problem=problem)
        if hit_statistic is None:
            raise Exception()
    except:
        http_referer = request.META.get('HTTP_REFERER')
        data_cont = {
            "title": "404",
            "msg": "页面没找到",
            "next_page": http_referer if http_referer is not None else '/index',
        }
        # raise Http404
        return render(request, "mixojapp/msg.html", data_cont)
    data_cont = {
        "title": "Statistics",
        "statistic": hit_statistic.get_statistics(),
    }
    # print(data_cont["statistic"])
    return render(request, "mixojapp/statistics.html", data_cont)
    pass


def update_problems(request):
    if request.method != "POST":
        return JsonResponse({"title": "404", "res": "error", "msg": "访问的页面不存在"})

    problems = request.POST.getlist('problems[]')
    if problems is None:
        return JsonResponse({"res": "error", "msg": "没有接收到要更新的题目."})

    for problem_id in problems:
        update_problem_by_id(problem_id)

    return JsonResponse({"res": "success"})
    pass


def crawling(request):
    data = {}
    ojs = OJ.objects.only("name")
    data["ojs"] = ojs
    return render(request, 'mixojapp/craw.html', data)
    pass


def craw_problem(request):
    """重新爬取/更新题目"""
    data = {}
    oj_name = request.POST.get("ojName")
    problem_id = request.POST.get("problemID")
    try:
        res = api_craw_problem(oj_name=oj_name, problem_id=problem_id)
        data["res"] = res.get("res")
        data["msg"] = res.get("msg")
        pass
    except Exception as e:
        import traceback
        traceback.print_exc()

        data["res"] = "error"
        data["msg"] = "爬取 " + str(oj_name) + " " + str(problem_id) + " 时出错:" + str(e)
        pass
    return JsonResponse(data)
    pass


def change_order(request):
    Order = ""
    Source = ""
    if request.method == 'POST':
        Ojname = request.POST.get("Ojname")
        Problem_id = request.POST.get("ProbNum")
        Title = request.POST.get("Title")
        Order = request.POST.get("Order")
        Source = request.POST.get("Source")
        Problem_type = request.POST.get("Problem_type")
    print(Source)
    if Order == "Problme_ASC" or Order is None:
        problems = Problem.objects.all().order_by("ojname", "sourceid")
    elif Order == "Problem_DESC":
        problems = Problem.objects.all().order_by("-sourceid")
    elif Order == "Total_ac_ASC":
        problems = Problem.objects.all().order_by("ac_rate")
    elif Order == "Total_ac_DESC":
        print("Total_ac_DESC")
        problems = Problem.objects.all().order_by("-ac_rate")
        print(len(problems))
    elif Order == "User_ac_ASC":
        problems = Problem.objects.all().order_by("user_ac_rate")
    elif Order == "User_ac_DESC":
        problems = Problem.objects.all().order_by("-user_ac_rate")
    elif Order == "Updata_time_ASC":
        problems = Problem.objects.all().order_by("Updata_time")
    elif Order == "Updata_time_DESC":
        problems = Problem.objects.all().order_by("-Updata_time")
    print("===1===")
    print(len(problems))
    print("===1===")
    if Ojname != "All":
        problems = problems.filter(ojname__exact=Ojname)
        print("===2===")
        print(len(problems))
        print("===2===")
    if Title is not None:
        problems = problems.filter(title__exact=Title)
        print("===3===")
        print(len(problems))
        print("===3===")
    if Source is not None and Source != "":
        problems = problems.filter(source__exact=Source)
        print("===4===")
        print(len(problems))
        print("===4===")
    if Problem_type is not None and Problem_type != "":
        problems = problems.filter(knowledge__exact=Problem_type)
        print("===5===")
        print(len(problems))
        print("===5===")
    if Problem_id is not None and Problem_id != "":
        problems = problems.filter(sourceid__exact=Problem_id)

    after_range_num = 5
    bevor_range_num = 4
    # 分页
    # 每页记录数
    problem_cnt_per_page = 20
    problem_page_list = Paginator(problems, problem_cnt_per_page)
    total_pages = problem_page_list.num_pages
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    try:
        # 尝试获得分页列表
        problems_cur_page = problem_page_list.page(page)
    except EmptyPage:
        # 获得最后一页
        problems_cur_page = problem_page_list.page(problem_page_list.num_pages)
    # 如果不是一个整数
    except PageNotAnInteger:
        # 获得第一页
        problems_cur_page = problem_page_list.page(1)
    if page >= after_range_num:
        page_range = problem_page_list.page_range[page - after_range_num:page + bevor_range_num]
    else:
        page_range = problem_page_list.page_range[0:page + bevor_range_num]
    data_cont = {
        "page1st": page - 2,
        "page2ed": page - 1,
        "page3th": page,
        "page4th": page + 1 if page + 1 <= total_pages else 0,
        "page5th": page + 2 if page + 2 <= total_pages else 0,
        "page_last": total_pages,

        "title": "Problem List",
        "problems": problems_cur_page,
        "page_range": page_range,
    }

    return render(request, "mixojapp/problemlist.html", data_cont)


def problem_list_datatables(request, oj_name="all"):
    data = {}
    oj_name_lower = str(oj_name).lower()
    if oj_name_lower != "all":
        problems = Problem.objects.filter(ojname__iexact=oj_name)
    else:
        problems = Problem.objects.all()
    # length = int(request.POST.get("length"))
    # data["recordsTotal"] = len(problems)
    # problems = list(problems)[0:length]
    # data["draw"] = request.POST.get("draw")
    # data["recordsFiltered"] = len(problems)

    res_problem = []
    for problem in problems:
        _t_problem = get_datatables_row(problem)
        res_problem.append(_t_problem)
        pass
    data["data"] = res_problem
    return JsonResponse(data)
    pass


def get_problem_by_knowledge(request, knowledgeid=-1):
    data = {}
    problems = Problem.objects.filter(knowledge_tree_node_id=knowledgeid)
    res_problem = []
    for problem in problems:
        _t_problem = get_datatables_row(problem)
        res_problem.append(_t_problem)
        pass
    data["data"] = res_problem
    return JsonResponse(data)
    pass


def get_problem_by_id_oj(request, problem_id, oj_name):
    data = {}
    problem_id = int(problem_id)
    problems = Problem.objects.filter(ojname__iexact=oj_name, sourceid=problem_id)
    res_problem = []
    for problem in problems:
        _t_problem = get_datatables_row(problem)
        res_problem.append(_t_problem)
        pass
    data["data"] = res_problem
    return JsonResponse(data)
    pass


def get_datatables_row(problem):
    _knowledge_tree = "<a onclick='javascript:getProblemByKnowledge(%s)' href='javascript:void(0)'>%s</a>"
    _problem_title = "<a href='/problemid/%s'>%s</a>" % (problem.id, problem.title)
    _hot_degree = problem.hot_degree
    _difficult_degree = problem.difficult
    _source = str(problem.source)
    _source = re.sub(r"<[^>]+>", "", _source)
    _source = re.sub(r"</[^>]+>", "", _source).strip()
    # print(_source)
    if _source is None or _source == "None" or _source == "":
        _source = "Unkonwn"
    _source = "<a onclick='javascript:search_source(\"%s\")' href='javascript:void(0)'>%s</a>" % (_source, _source)
    _t_problem = [problem.ojname,
                  problem.sourceid,
                  _problem_title,
                  problem.ac_rate,
                  problem.user_ac_rate,
                  get_degree_star(_difficult_degree, reverse=True),
                  get_degree_star(_hot_degree),
                  _source,
                  problem.update_time,
                  _knowledge_tree % (problem.knowledge_tree_node_id, problem.knowledge_tree_node_name),
                  ]
    return _t_problem
    pass


def get_degree_star(_degree, reverse=False):
    try:
        _degree = float(_degree)
        if _degree < -1.5:
            _degree_res = 1
        elif _degree < -0.5:
            _degree_res = 2
        elif _degree < 0.5:
            _degree_res = 3
        elif _degree < 1.5:
            _degree_res = 4
        else:
            _degree_res = 5
        pass
    except:
        return ""
        pass
    if reverse:
        return "&#9830;" * (6 - _degree_res)
    else:
        return "&#9830;" * _degree_res
    pass


def get_problems_by_source(request, source_title):
    data = {}
    problems = []
    _problems_list = get_problems_by_source_title(source_title)
    # print(_problems_list)
    for t_problem in _problems_list:
        try:
            _query_problems = Problem.objects.filter(ojname=t_problem.get("ojname"), sourceid=t_problem.get("id"))
            for _query_problem in _query_problems:
                _t_res_problem = get_datatables_row(_query_problem)
                problems.append(_t_res_problem)
            pass
        except:
            pass
        pass
    data["data"] = problems
    return JsonResponse(data)
    pass


def update_hot_and_difficult_degree_view(request):
    try:
        update_hot_and_difficult_degree()
    except Exception as e:
        print("更新热度时出错：", e)
        pass
    return JsonResponse({})
    pass


def chuti(request):
    data = {}
    # print(request.POST)

    oj = request.POST.get("oj")
    difficult = request.POST.get("difficult")
    hot= request.POST.get("hot")
    knowledge = request.POST.get("knowledge")
    number = request.POST.get("number")

    problems = aotu_problems(ojname=oj, hot_degrees=hot, dif_degrees=difficult, nums=number, knowledge=knowledge)
    # print(problems)
    for problem in problems:
        problem.difficult = get_degree_star(problem.difficult)
        problem.hot_degree= get_degree_star(problem.hot_degree)

    knowledges = get_all_knowledge_node_name()
    ojs = OJ.objects.all()
    data["ojs"] = ojs
    data["problems"] = problems
    data["knowledges"] = knowledges
    return render(request, 'mixojapp/chuti.html', data)
    pass
