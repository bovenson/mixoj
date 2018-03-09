# coding:utf-8
from spider.stagetwo.db.db_operations import get_old_urls
from spider.stagetwo.public.url_manager import UrlManager
from spider.stagetwo.public.html_downloader import HtmlDownloader
from spider.stagetwo.public.html_outputer import HtmlOutputer
from spider.stagetwo.parser.parser_manager import get_parser

PAGE_CNT_TO_CRAW = -1

FIRST_CRAW = 1
UPDATE = 2


class OjSpider(object):
    @staticmethod
    # def runspider(oj_name, root_url, page_to_craw=PAGE_CNT_TO_CRAW, operation=FIRST_CRAW):
    def runspider(oj_name, root_url, operation=FIRST_CRAW):
        urls = UrlManager()
        outputer = HtmlOutputer()
        # 添加起始 url
        urls.add_new_url(root_url)
        # 如果是第一次录入数据库操作, 那么就不在抓取已经爬取的题目, 以便有些题目抓取失败, 不用再重新爬取
        if operation == FIRST_CRAW:
            # 记录已经爬取的页面
            old_urls = get_old_urls(oj_name)
            urls.add_old_urls(old_urls)
        cur_url = ""
        page_count = 0
        while urls.has_url():
            try:
                # 取待爬取 url
                cur_url = urls.get_new_url()
                # 下载得到二进制的页面
                html_content = HtmlDownloader.download(cur_url)
                if html_content is None:
                    print("爬取页面 %s 时出错:连接超时" % cur_url)
                    urls.add_new_url(cur_url)
                    continue
                # 新建分析器
                oj_parser = get_parser(oj_name, cur_url, html_content)

                oj_parser.html_content = html_content
                # 从分析器中得到数据
                new_problem = oj_parser.get_problem()
                # 保存数据
                # 如果不是第一次爬取, 不添加新的url
                if operation == FIRST_CRAW:
                    new_urls = oj_parser.get_urls()
                    if new_urls is not None:
                        urls.add_new_urls(new_urls)
                        pass
                if new_problem is not None:
                    # 得到当前问题的提交信息
                    problem_statistic = oj_parser.get_status()

                    outputer.save_to_db(problem=new_problem, statistic=problem_statistic, operation=operation)

                    pass
                pass
            except Exception as e:
                print("爬取页面 %s 时出错:" % cur_url, e)
                import traceback
                print(traceback.format_exc())
                pass
            else:
                print("爬取页面 %s 成功." % cur_url)
                pass
            pass
        pass

    @staticmethod
    def runspider_by_id(oj_name, cur_url):
        operation = FIRST_CRAW
        # urls = UrlManager()
        outputer = HtmlOutputer()
        old_urls = get_old_urls(oj_name)
        if cur_url in old_urls:
            operation = UPDATE
        else:
            try:
                html_content = HtmlDownloader.download(cur_url)
                if html_content is None:
                    OjSpider.runspider_by_id(oj_name, cur_url)
                    return
                else:
                    oj_parser = get_parser(oj_name, cur_url, html_content)
                    new_problem = oj_parser.get_problem()
                    if new_problem is not None:
                        problem_statistic = oj_parser.get_status()
                        outputer.save_to_db(problem=new_problem, statistic=problem_statistic, operation=operation)
                        _res = "success"
                        return
                        pass

            except Exception as e:
                _res = "error"
                return _res

    @staticmethod
    def craw_one_page(oj_name, problem_id, cur_url):
        _res = {}
        try:
            # 下载得到二进制的页面
            html_content = HtmlDownloader.download(cur_url)
            if html_content is None:
                _res["res"] = "error"
                _res["msg"] = "连接超时，请重新下载题目"
                return _res
            # 新建分析器
            oj_parser = get_parser(oj_name, cur_url, html_content)
            oj_parser.html_content = html_content
            # 从分析器中得到数据
            new_problem = oj_parser.get_problem()
            # 保存数据
            if new_problem is not None:
                # 得到当前问题的提交信息
                problem_statistic = oj_parser.get_status()
                outputer = HtmlOutputer()
                outputer.save_to_db_auto(ojname=oj_name, problem_id=problem_id, problem=new_problem,
                                         statistic=problem_statistic)
            # 爬虫主程序 end
            pass
        except Exception as e:
            print("爬取:", cur_url, " 时出错")
            import traceback
            traceback.print_exc()
            _res["res"] = "error"
            error_msg = str(e)
            if error_msg.find("urlopen error"):
                _res["msg"] = "下载失败,可能题目不存在/网络错误"
            elif error_msg.find("NoneType"):
                _res["msg"] = "页面解析失败,可能题目不存在/原网页结构改变"
            else:
                _res["msg"] = "爬取失败:" + error_msg
            pass
        else:
            _res["res"] = "success"
            _res["msg"] = "爬取成功"
        return _res

    pass
