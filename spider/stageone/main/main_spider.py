# coding:utf-8
from spider.stageone.db.db_operations import get_old_urls
from spider.stageone.public.url_manager import UrlManager
from spider.stageone.public.html_downloader import HtmlDownloader
from spider.stageone.public.html_outputer import HtmlOutputer
from spider.stageone.parser.parser_manager import get_parser

PAGE_CNT_TO_CRAW = -1

FIRST_CRAW = 1
UPDATE = 2


class OjSpider(object):
    @staticmethod
    def runspider(oj_name, root_url, page_to_craw=PAGE_CNT_TO_CRAW, operation=FIRST_CRAW):
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
                    # 计算 AC 率
                    # if new_status is not None and new_status.get("total_sub") is not None:
                    #     if int(new_status.get("total_sub")) != 0:
                    #         ac_rate = float(new_status.get("ac")) / float(new_status.get("total_sub"))
                    #         ac_rate = str("%.2f%%" % ac_rate)
                    #         new_problem["ac_rate"] = ac_rate
                    # 保存问题
                    # outputer.save_problem_to_db(new_problem)
                    # 保存问题信息
                    # outputer.save_status_to_db(new_status)
                    # 保存问题及数据
                    outputer.save_to_db(problem=new_problem, statistic=problem_statistic, operation=operation)
                    page_count += 1
                # 爬虫主程序 end

                # 设置计数, 测试用
                # page_count += 1
                if 0 < page_to_craw < page_count:
                    break
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
    def craw_one_page(oj_name, problem_id, cur_url):
        _res = {}
        try:
            # 下载得到二进制的页面
            html_content = HtmlDownloader.download(cur_url)
            # 新建分析器
            oj_parser = get_parser(oj_name, cur_url, html_content)
            oj_parser.html_content = html_content
            # 从分析器中得到数据
            new_problem = oj_parser.get_problem()
            # 保存数据
            if new_problem is not None:
                # 得到当前问题的提交信息
                problem_statistic = oj_parser.get_status()
                # 计算 AC 率
                # if new_status is not None and new_status.get("total_sub") is not None:
                #     if int(new_status.get("total_sub")) != 0:
                #         ac_rate = float(new_status.get("ac")) / float(new_status.get("total_sub"))
                #         ac_rate = str("%.2f%%" % ac_rate)
                #         new_problem["ac_rate"] = ac_rate
                # 保存问题
                # outputer.save_problem_to_db(new_problem)
                # 保存问题信息
                # outputer.save_status_to_db(new_status)
                # 保存问题及数据
                outputer = HtmlOutputer()
                outputer.save_to_db_auto(ojname=oj_name, problem_id=problem_id, problem=new_problem, statistic=problem_statistic)
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

