# coding: utf-8
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../..')))

from spider.stageone.main.main_spider import OjSpider
from spider.stageone.main.main_spider import FIRST_CRAW

PAGE_TO_CRAW = 30


class StartSpider(object):
    @staticmethod
    def crawling_poj():
        # 抓取 Poj
        oj_name = "Poj"
        root_url = "http://poj.org/problemlist"
        OjSpider.runspider(oj_name=oj_name, root_url=root_url, page_to_craw=PAGE_TO_CRAW, operation=FIRST_CRAW)
        pass

    @staticmethod
    def crawling_zoj():
        # 抓取 Zoj
        oj_name = "Zoj"
        root_url = "http://acm.zju.edu.cn/onlinejudge/showProblemsets.do"
        # root_url = "http://acm.zju.edu.cn/onlinejudge/showProblem.do?problemCode=1056"
        OjSpider.runspider(oj_name=oj_name, root_url=root_url, page_to_craw=PAGE_TO_CRAW, operation=FIRST_CRAW)
        pass

    @staticmethod
    def crawling_sgu():
        # 抓取 Sgu
        oj_name = "Sgu"
        root_url = "http://acm.sgu.ru/problemset.php?show_volumes"
        OjSpider.runspider(oj_name=oj_name, root_url=root_url, page_to_craw=PAGE_TO_CRAW, operation=FIRST_CRAW)
        pass

    @staticmethod
    def crawling_uvalive():
        # 抓取 UVALive
        oj_name = "UVALive"
        root_url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8"
        OjSpider.runspider(oj_name=oj_name, root_url=root_url, page_to_craw=PAGE_TO_CRAW, operation=FIRST_CRAW)
        pass

    @staticmethod
    def crawling_all():
        # StartSpider.crawling_poj()
        # StartSpider.crawling_zoj()
        # StartSpider.crawling_sgu()
        StartSpider.crawling_uvalive()
        pass
    pass


if __name__ == "__main__":
    # print(sys.path)
    StartSpider.crawling_all()
    # 抓取 Poj
    # oj_name = "Poj"
    # root_url = "http://poj.org/problemlist"
    # OjSpider.runspider(oj_name=oj_name, root_url=root_url, page_to_craw=10, operation=FIRST_CRAW)
    #
    # # 抓取 UVALive
    # oj_name = "UVALive"
    # root_url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8"
    # OjSpider.runspider(oj_name=oj_name, root_url=root_url, page_to_craw=10, operation=FIRST_CRAW)
    #
    # # 抓取 Sgu
    # oj_name = "Sgu"
    # root_url = "http://acm.sgu.ru/problemset.php?show_volumes"
    # OjSpider.runspider(oj_name=oj_name, root_url=root_url, page_to_craw=10, operation=FIRST_CRAW)
    #
    # # 抓取 Zoj
    # oj_name = "Zoj"
    # root_url = "http://acm.zju.edu.cn/onlinejudge/showProblemsets.do"
    # # root_url = "http://acm.zju.edu.cn/onlinejudge/showProblem.do?problemCode=1056"
    # OjSpider.runspider(oj_name=oj_name, root_url=root_url, page_to_craw=10, operation=FIRST_CRAW)
    #
    # root_url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=617&page=show_problem&problem=4476"
    # root_url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=461&page=show_problem&problem=3608"
    # root_url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=617&page=show_problem&problem=4476"
    # root_url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=186&page=show_problem&problem=1264"
    # root_url = "http://localhost:8080/oj/uvalive/option=com_onlinejudge&Itemid=8&category=26&page=show_problem&problem=2309.html"
    # spider = OjSpider()
    # root_url="https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8"
    # spider.runspider(oj_name="UVALive", root_url=root_url)

    # 抓取Zoj
    # spider = OjSpider()
    # spider.runspider(oj_name="Zoj", root_url="http://acm.zju.edu.cn/onlinejudge/showProblemsets.do")

    # 抓取Sgu
    # root_url = "http://acm.sgu.ru/problem.php?contest=0&problem=115"
    # spider = OjSpider()
    # root_url="http://acm.sgu.ru/problemset.php?show_volumes"


    pass
