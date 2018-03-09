# coding: utf-8
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../..')))

from spider.main.main_spider import OjSpider
from spider.main.main_spider import FIRST_CRAW, UPDATE
from knowledge_tree.db.db_initdb import init_db
from knowledge_tree.db.build_tree import build_tree
from spider.main.degree import degree

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
    def crawling_hysbz():
        # 抓取 Sgu
        oj_name = "Hysbz"
        root_url = "http://www.lydsy.com/JudgeOnline/problemset.php?page=1"
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
    def crawling_ural():
        # 抓取 UVALive
        oj_name = "Ural"
        root_url = "http://acm.timus.ru/problemset.aspx?space=1&page=all"
        OjSpider.runspider(oj_name=oj_name, root_url=root_url, page_to_craw=PAGE_TO_CRAW, operation=FIRST_CRAW)
        pass
    @staticmethod
    def crawling_hust():
        # 抓取 UVALive
        oj_name = "Hust"
        root_url = "http://acm.hust.edu.cn/problem/list/1"
        OjSpider.runspider(oj_name=oj_name, root_url=root_url, page_to_craw=PAGE_TO_CRAW, operation=FIRST_CRAW)
        pass
    @staticmethod
    def crawling_hdu():
        # 抓取 UVALive
        oj_name = "Hdu"
        root_url = "http://acm.hdu.edu.cn/listproblem.php?vol=1"
        OjSpider.runspider(oj_name=oj_name, root_url=root_url, page_to_craw=PAGE_TO_CRAW, operation=FIRST_CRAW)
        pass
    @staticmethod
    def crawling_codeforces():
        # 抓取 UVALive
        oj_name = "CodeForces"
        root_url = "http://codeforces.com/problemset/page/1"
        OjSpider.runspider(oj_name=oj_name, root_url=root_url, page_to_craw=PAGE_TO_CRAW, operation=FIRST_CRAW)
        pass
    @staticmethod
    def init_trees(ojname):
        init_db()
        build_tree()
    def crawling_all_by_ojname(ojname):
        oj_name = str(ojname).lower()
        if oj_name == "poj":
            StartSpider.crawling_poj()
        elif oj_name == "uvalive":
            StartSpider.crawling_uvalive()
        elif oj_name == "sgu":
            StartSpider.crawling_sgu()
        elif oj_name == "zoj":
            StartSpider.crawling_zoj()
        elif oj_name=="ural":
            StartSpider.crawling_ural()
        elif oj_name=="hust":
            StartSpider.crawling_hust()
        elif oj_name=="hysbz":
            StartSpider.crawling_hysbz()
        elif oj_name=="hdu":
            StartSpider.crawling_hdu()
        elif oj_name=="codeforces":
            StartSpider.crawling_codeforces()



if __name__ == "__main__":
   m=StartSpider
   #m.crawling_all_by_ojname("Sgu")
   degree("Sgu")
