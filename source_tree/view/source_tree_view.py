from mixojapp.models import Problem, OJ
from source_tree.db.db_operations import get_source_tree_json, addNode, deleteNodeByName, \
    findParentByName, addProblem, findRef
from source_tree.build_source_tree import updateProblem
from django.shortcuts import render
from django.http import JsonResponse

def source_tree(request):
    data = {}
    ojs = OJ.objects.only("name")
    data["ojs"] = ojs
    return render(request, "mixojapp/source_tree.html", data)

def get_source_tree(request):
    level = request.POST.get('Level')
    date = request.POST.get('Date')
    if level is None or level == 'All':
        level = '%'
    if date is None or date == 'All':
        date = '%'
    data = get_source_tree_json(level,date)
    return JsonResponse({"data": data})

def source_tree_node_edit(request):
    data = {}
    try:
        action = request.POST.get("action")
        if action == "show":
            node_id = request.POST.get("nodeId")
            # data = get_node_detail_by_id(node_id)
            pass
        elif action == "add-child":
            node_id = request.POST.get("nodeId")
            node_name = request.POST.get("nodeName")
            res = addNode(node_name, node_id)
            data["res"] = res.get('res')
            data["msg"] = res.get("msg")
            pass
        elif action == "add-brother":
            node_id = request.POST.get("nodeId")
            node_name = request.POST.get("nodeName")
            pid = findParentByName(node_id)
            res = addNode(node_name,pid)
            data["res"] = res.get('res')
            data["msg"] = res.get("msg")
            pass
        elif action == "delete":
            node_id = request.POST.get("nodeId")
            res = deleteNodeByName(node_id)
            data["res"] = res.get('res')
            data["msg"] = res.get("msg")
            pass
        elif action == "add-problem":
            node_id = request.POST.get("nodeID")
            node_name = request.POST.get("nodeName")
            oj_name = request.POST.get("ojName")
            problem_id = request.POST.get("problemID")
            try:
                res = addProblem(problem_id, oj_name, node_id)
                data["res"] = res.get('res')
                data["msg"] = res.get("msg")
                # updateProblem('%', '%')
                pass
            except Problem.DoesNotExist:
                data["res"] = "error"
                data["msg"] = "没有找到题目"
                pass
            pass
    except:
        data["res"] = "error"
        data["msg"] = "操作出错"
        pass
    return JsonResponse(data)
    pass


def update_nodes(request):
    _data = {}
    problem_id = request.POST.get("problemID")
    oj_name = request.POST.get("ojName")
    try:
        if problem_id is None:
            _data["res"] = "error"
            _data["msg"] = "没有发送题目ID"
            raise Exception()
        if oj_name is None:
            _data["res"] = "error"
            _data["msg"] = "没有发送OJ名称"
            raise Exception()
        _res = updateProblem(problem_id, oj_name)
        _data["res"] = _res.get("res")
        _data["msg"] = _res.get("msg")
        pass
    except Exception as e:
        if _data.get("res") is None:
            _data["res"] = "error"
            _data["msg"] = "更新" + str(problem_id) + "失败:" + str(e)
        pass
    return JsonResponse(_data)
    pass
