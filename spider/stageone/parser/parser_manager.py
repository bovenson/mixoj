# codding: utf-8
from spider.stageone.parser.poj.html_parser_poj import PojHtmlParser
from spider.stageone.parser.sgu.html_parser_sgu import SguHtmlParser
from spider.stageone.parser.uvalive.html_parser_uvalive import UVALiveHtmlParser
from spider.stageone.parser.zoj.html_parser_zoj import ZojHtmlParser


def get_parser(oj_name, page_url, html_content):
    """根据 OJ 名返回相应parser
    :param html_content:二进制的网页内容
    :param oj_name:OJ名
    """
    parser = None
    # 忽略大小写
    oj_name = str(oj_name).lower()
    if oj_name == "poj":
        parser = PojHtmlParser(page_url, html_content)
    elif oj_name == "uvalive":
        parser = UVALiveHtmlParser(page_url, html_content)
    elif oj_name == "sgu":
        parser = SguHtmlParser(page_url, html_content)
    elif oj_name == "zoj":
        parser = ZojHtmlParser(page_url, html_content)
    else:
        raise Exception("未知的OJ名称")
    return parser
    pass
