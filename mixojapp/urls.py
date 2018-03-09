from django.conf.urls import url
import mixojapp.views as views
from knowledge_tree.view import knowledge_tree_view
from source_tree.view import source_tree_view

urlpatterns = [
    # 打开列表的url
    url(r'^page/(?P<page>[0-9]+)/*$', views.problem_list, name="problemlist_given_pageno"),
    url(r'^problemlist/ojname/(?P<oj_name>[a-zA-Z0-9 ]*)/*$', views.problem_list_datatables),
    url(r'^problemlist/knowledge/(?P<knowledgeid>[\-0-9]*)/*$', views.get_problem_by_knowledge),

    url(r'^chuti/*$', views.chuti, name="chuti"),
    # 打开问题的url
    url(r'^problemid/(?P<problemid>[0-9]+)/*$', views.show_problem, name="problemdetail"),

    # 问题数据信息url
    url(r'^statistics/(?P<problemid>[0-9]+)/*$', views.show_statistics, name="show_statistics"),

    # 更新题目信息
    url(r'update_problems/*$', views.update_problems, name="update_problems"),

    # 更新难度及热度
    url(r'^update_hot_and_difficult_degree/*$', views.update_hot_and_difficult_degree_view,
        name="update_hot_and_difficult_degree"),

    # 爬取题目
    url(r'crawling/*$', views.crawling, name="crawling"),
    url(r'crawproblem/*$', views.craw_problem, name="craw_problem"),

    # 知识树
    url(r'knowledgetree/*$', knowledge_tree_view.knowledge_tree, name="knowledge_tree"),
    url(r'get_knowledge_tree/*$', knowledge_tree_view.get_knowledge_tree, name="get_knowledge_tree"),
    url(r'knowledgetree/edit/*$', knowledge_tree_view.knowledge_tree_node_edit, name="knowledge_tree_node_edit"),
    url(r'knowledgetree/updatenodes/*$', knowledge_tree_view.update_nodes, name="knowledge_tree_update_nodes"),

    url(r'^change_order/*$', views.change_order , name="change_order"),

    # 来源树
    url(r'sourcetree/*$', source_tree_view.source_tree, name="source_tree"),
    url(r'get_source_tree/*$', source_tree_view.get_source_tree, name="get_source_tree"),
    url(r'sourcetree/edit/*$', source_tree_view.source_tree_node_edit, name="source_tree_node_edit"),
    url(r'sourcetree/updatenodes/*$', source_tree_view.update_nodes, name="source_tree_update_nodes"),

    url(r'^problemlist/sourcetree/pid/(?P<problem_id>[\d]+)/oj/(?P<oj_name>[a-zA-Z0-9]+)/*$', views.get_problem_by_id_oj),
    url(r'^problemlist/sourcetree/title/(?P<source_title>[\w\W]+)/*$', views.get_problems_by_source),

    # 未识别url
    url(r'', views.problem_list, name="problemlist"),
]
