# coding: utf-8
import time
from django.shortcuts import render
from django.http import JsonResponse

from knowledge_tree.db.db_operations import get_knowledge_tree_json, get_node_detail_by_id, update_node, add_child_node, \
    get_parent_id_by_id, delete_knowledge_tree_node, add_node
from knowledge_tree.main.entry import update_problem_knowledge_tree
from mixojapp.models import Problem, OJ


def knowledge_tree(request):
    data = {}
    ojs = OJ.objects.only("name")
    data["ojs"] = ojs
    return render(request, "mixojapp/knowledge_tree.html", data)


def get_knowledge_tree(request):
    # data = [{"text": "root"}]
    data = get_knowledge_tree_json()
    if len(data) == 0:
        add_node(_pid=-1, _name="其他")
        data = get_knowledge_tree_json()
    return JsonResponse({"data": data})
    pass


def knowledge_tree_node_edit(request):
    data = {}
    try:
        action = request.POST.get("action")
        if action == "show":
            node_id = request.POST.get("nodeId")
            data = get_node_detail_by_id(node_id)
            pass
        elif action == "add-child":
            node_id = request.POST.get("nodeId")
            node_name = request.POST.get("nodeName")
            node_synonym = request.POST.get("nodeSynonym")
            res = add_child_node(_pid=node_id, _node_name=node_name, _node_synonym=node_synonym)
            data["res"] = res.get('res')
            data["msg"] = res.get("msg")
            pass
        elif action == "add-brother":
            node_id = request.POST.get("nodeId")
            node_name = request.POST.get("nodeName")
            node_synonym = request.POST.get("nodeSynonym")
            pid = get_parent_id_by_id(node_id)
            # print("node id：", node_id, "pid:", pid)
            res = add_child_node(_pid=pid, _node_name=node_name, _node_synonym=node_synonym)
            data["res"] = res.get('res')
            data["msg"] = res.get("msg")
            pass
        elif action == "update":
            node_id = request.POST.get("nodeId")
            node_name = request.POST.get("nodeName")
            node_synonym = request.POST.get("nodeSynonym")
            res = update_node(_node_id=node_id, _node_name=node_name, _node_synonym=node_synonym)
            data["res"] = res.get('res')
            data["msg"] = res.get("msg")
            pass
        elif action == "delete":
            node_id = request.POST.get("nodeId")
            res = delete_knowledge_tree_node(_node_id=node_id)
            data["res"] = res.get('res')
            data["msg"] = res.get("msg")
            pass
        elif action == "add-problem":
            node_id = request.POST.get("nodeID")
            node_name = request.POST.get("nodeName")
            oj_name = request.POST.get("ojName")
            problem_id = request.POST.get("problemID")
            try:
                problem = Problem.objects.get(sourceid=problem_id, ojname=oj_name)
                problem.knowledge_tree_node_name = node_name
                problem.knowledge_tree_node_id = node_id
                problem.save()
                data["res"] = "success"
                data["mgs"] = "更新成功"
                pass
            except Problem.DoesNotExist:
                data["res"] = "error"
                data["msg"] = "没有找到题目"
                pass
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
        _res = update_problem_knowledge_tree(oj_name, problem_id)
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
