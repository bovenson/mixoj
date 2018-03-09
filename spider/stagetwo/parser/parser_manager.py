# codding: utf-8
from spider.stagetwo.parser.poj.html_parser_poj import PojHtmlParser
from spider.stagetwo.parser.sgu.html_parser_sgu import SguHtmlParser
from spider.stagetwo.parser.uvalive.html_parser_uvalive import UVALiveHtmlParser
from spider.stagetwo.parser.zoj.html_parser_zoj import ZojHtmlParser
from spider.stagetwo.parser.ural.html_parser_ural import UralHtmlPaser
from spider.stagetwo.parser.hust.html_parser_hust import HustHtmlParser
from spider.stagetwo.parser.hysbz.html_parser_hysbz import HysbzHtmlParser
from spider.stagetwo.parser.hdu.html_parser_hdu import HduHtmlParser
from spider.stagetwo.parser.codeforces.html_parser_codeforces import CodeHtmlParser
from spider.stagetwo.parser.uva.html_parser_uva import UVALiveHtmlParser as UvaParser
from spider.stagetwo.parser.spoj.html_parser_spoj import SpojHtmlParser


def get_parser(oj_name, page_url, html_content):
    """根据 OJ 名返回相应parser
    :param page_url:
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
    elif oj_name == "ural":
        parser = UralHtmlPaser(page_url, html_content)
    elif oj_name == "hust":
        parser = HustHtmlParser(page_url, html_content)
    elif oj_name == "hysbz":
        parser = HysbzHtmlParser(page_url, html_content)
    elif oj_name == "hdu":
        parser = HduHtmlParser(page_url, html_content)
    elif oj_name == "codeforces":
        parser = CodeHtmlParser(page_url, html_content)
    elif oj_name == "uva":
        parser = UvaParser(page_url, html_content)
    elif oj_name == "spoj":
        parser = SpojHtmlParser(page_url, html_content)
    else:
        raise Exception("未知的OJ名称")
    return parser
    pass
