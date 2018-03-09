# codding: utf-8
from mixojapp.models import Problem
from spider.stageone.main.main_spider import UPDATE, OjSpider
from spider.stageone.main.start_spider import StartSpider


def update_problem_by_id(problem_id):
    if problem_id is None:
        return
    # print(problem_id)
    problem = Problem.objects.get(id=problem_id)
    oj_name = problem.ojname
    url = problem.url
    OjSpider.runspider(oj_name=oj_name, root_url=url, page_to_craw=1, operation=UPDATE)
    return
    pass


def start_crawling():
    StartSpider.crawling_all()
    pass
